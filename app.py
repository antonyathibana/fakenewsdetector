"""
Fake News Detection Web Application
Main Flask Application with Hybrid Verification System
"""

import pickle
import re
import string
import logging
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from pathlib import Path
import config
from database import (
    init_db, save_prediction, get_history, 
    get_prediction_by_id, get_total_count, get_stats, clear_history
)
from preprocess_data import preprocess_text

# Initialize Flask app
app = Flask(__name__)
app.secret_key = config.SECRET_KEY

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global variables for model and vectorizer
model = None
vectorizer = None


def load_model():
    """
    Load the trained model and vectorizer from pickle files
    """
    global model, vectorizer
    
    try:
        with open(config.MODEL_PATH, 'rb') as f:
            model = pickle.load(f)
        
        with open(config.VECTORIZER_PATH, 'rb') as f:
            vectorizer = pickle.load(f)
        
        print("✓ Model and vectorizer loaded successfully")
        return True
        
    except FileNotFoundError:
        print("❌ Model files not found!")
        print("Please run: python train_model.py")
        return False
    except Exception as e:
        print(f"❌ Error loading model: {e}")
        return False


def check_fact_check_api(query_text):
    """
    Check facts using Google Fact Check API
    
    Args:
        query_text: Text to search for fact checks
    
    Returns:
        dict: Fact check results or error information
    """
    # Check if API key is configured
    if not config.GOOGLE_FACT_CHECK_API_KEY:
        logger.info("Google Fact Check API key not configured")
        return {
            'enabled': False,
            'error': 'API key not configured',
            'claims': []
        }
    
    try:
        # Use first 200 characters for search
        query = query_text[:200].strip()
        
        # API request parameters
        params = {
            'key': config.GOOGLE_FACT_CHECK_API_KEY,
            'query': query,
            'maxAgeDays': 90,  # Get claims from last 90 days
            'pageSize': 5,  # Limit results
            'languageCode': 'en'  # Only English results
        }
        
        # Make API request
        import requests
        response = requests.get(
            config.GOOGLE_FACT_CHECK_API_URL,
            params=params,
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            
            claims = []
            if 'claims' in data and data['claims']:
                for claim in data['claims'][:5]:  # Limit to 5 claims
                    # Extract claim review information
                    claim_text = claim.get('text', '')
                    reviews = claim.get('claimReview', [])
                    
                    for review in reviews:
                        claim_info = {
                            'publisher': review.get('publisher', {}).get('name', 'Unknown'),
                            'url': review.get('url', '#'),
                            'rating': review.get('rating', {}).get('text', 'N/A'),
                            'rating_label': review.get('rating', {}).get('alternateName', 'N/A'),
                            'claim_date': claim.get('claimDate', ''),
                            'review_date': review.get('reviewDate', ''),
                            'claim_text': claim_text
                        }
                        claims.append(claim_info)
            
            return {
                'enabled': True,
                'success': True,
                'claims': claims,
                'query': query
            }
            
        elif response.status_code == 403:
            logger.warning("Google Fact Check API: Invalid API key")
            return {
                'enabled': True,
                'success': False,
                'error': 'Invalid API key',
                'claims': []
            }
        else:
            logger.error(f"Google Fact Check API error: {response.status_code}")
            return {
                'enabled': True,
                'success': False,
                'error': f'API error: {response.status_code}',
                'claims': []
            }
            
    except ImportError:
        logger.error("requests library not installed")
        return {
            'enabled': True,
            'success': False,
            'error': 'requests library not installed',
            'claims': []
        }
    except Exception as e:
        logger.error(f"Google Fact Check API: {str(e)}")
        return {
            'enabled': True,
            'success': False,
            'error': str(e),
            'claims': []
        }


def predict_news(text):
    """
    Predict whether news is fake or real
    
    Args:
        text: Input news text
    
    Returns:
        dict: Prediction result with confidence
    """
    # Check if model and vectorizer are loaded
    if model is None or vectorizer is None:
        return {
            'prediction': 'ERROR',
            'confidence': 0,
            'error': 'Model not loaded. Please run train_model.py first.'
        }
    
    if not text or len(text.strip()) < 10:
        return {
            'prediction': 'UNKNOWN',
            'confidence': 0,
            'error': 'Text is too short for prediction'
        }
    
    try:
        # Preprocess the text
        processed_text = preprocess_text(text)
        
        # Transform using TF-IDF
        text_tfidf = vectorizer.transform([processed_text])
        
        # Make prediction
        prediction = model.predict(text_tfidf)[0]
        
        # Get prediction probabilities
        probabilities = model.predict_proba(text_tfidf)[0]
        confidence = probabilities[prediction] * 100
        
        # Map prediction to label
        result = 'REAL' if prediction == 1 else 'FAKE'
        
        return {
            'prediction': result,
            'confidence': round(confidence, 2),
            'fake_probability': round(probabilities[0] * 100, 2),
            'real_probability': round(probabilities[1] * 100, 2)
        }
        
    except Exception as e:
        return {
            'prediction': 'ERROR',
            'confidence': 0,
            'error': str(e)
        }


# ==================== ROUTES ====================

@app.route('/')
def index():
    """
    Home page route
    """
    stats = get_stats()
    predictions = get_history(limit=5)
    fact_check_enabled = bool(config.GOOGLE_FACT_CHECK_API_KEY)
    return render_template('index.html', stats=stats, predictions=predictions, fact_check_enabled=fact_check_enabled)


@app.route('/predict', methods=['POST'])
def predict():
    """
    Predict route - handles form requests for text input
    """
    # Check if it's a JSON request
    if request.is_json:
        data = request.get_json()
        news_text = data.get('text', '').strip()
        enable_fact_check = data.get('fact_check', True)
    else:
        # Form submission
        news_text = request.form.get('news_text', '').strip()
        enable_fact_check = request.form.get('enable_fact_check', 'true').lower() == 'true'
    
    # Validate input
    if not news_text:
        if request.is_json:
            return jsonify({'error': 'Please provide news text'}), 400
        flash('Please provide news text to analyze!', 'danger')
        return redirect(url_for('index'))
    
    # Make ML prediction
    result = predict_news(news_text)
    
    # Get fact check results if enabled
    fact_check_result = None
    if enable_fact_check:
        fact_check_result = check_fact_check_api(news_text)
    
    # Save to history
    if result['prediction'] != 'ERROR' and result['prediction'] != 'UNKNOWN':
        save_prediction(
            text=news_text[:10000],  # Store first 10000 chars
            prediction=result['prediction'],
            confidence=result['confidence'],
            is_url=False
        )
    
    # Return response based on request type
    if request.is_json:
        return jsonify({
            'prediction': result,
            'fact_check': fact_check_result
        })
    
    # For regular form submission, render result page
    if result['prediction'] == 'ERROR':
        flash(result.get('error', 'An error occurred'), 'danger')
        return redirect(url_for('index'))
    
    if result['prediction'] == 'UNKNOWN':
        flash(result.get('error', 'Text too short'), 'warning')
        return redirect(url_for('index'))
    
    return render_template('result.html', 
                          result=result, 
                          fact_check=fact_check_result,
                          input_type='text',
                          pred_class='fake' if result['prediction'] == 'FAKE' else 'real',
                          pred_icon='times' if result['prediction'] == 'FAKE' else 'check',
                          conf_color='danger' if result['prediction'] == 'FAKE' else 'success',
                          bg_class='bg-danger' if result['prediction'] == 'FAKE' else 'bg-success')


@app.route('/history')
def history():
    """
    View prediction history
    """
    page = request.args.get('page', 1, type=int)
    per_page = config.ITEMS_PER_PAGE
    offset = (page - 1) * per_page
    
    predictions = get_history(limit=per_page, offset=offset)
    total = get_total_count()
    total_pages = (total + per_page - 1) // per_page
    
    return render_template(
        'history.html',
        predictions=predictions,
        page=page,
        total_pages=total_pages,
        total=total,
        conf_color='danger'
    )


@app.route('/history/<int:prediction_id>')
def view_prediction(prediction_id):
    """
    View a specific prediction
    """
    prediction = get_prediction_by_id(prediction_id)
    
    if not prediction:
        flash('Prediction not found', 'warning')
        return redirect(url_for('history'))
    
    return render_template('view_prediction.html', prediction=prediction)


@app.route('/clear-history', methods=['POST'])
def clear_history_route():
    """
    Clear prediction history
    """
    clear_history()
    flash('History cleared successfully', 'success')
    return redirect(url_for('history'))


@app.errorhandler(404)
def not_found(error):
    """
    404 error handler
    """
    return render_template('error.html', error='Page not found'), 404


@app.errorhandler(500)
def internal_error(error):
    """
    500 error handler
    """
    return render_template('error.html', error='Internal server error'), 500


# ==================== MAIN ====================

if __name__ == '__main__':
    print("\n" + "=" * 50)
    print("🚀 Fake News Detection Web Application")
    print("=" * 50)
    
    # Initialize database
    print("\n📦 Initializing database...")
    init_db()
    
    # Load model
    print("\n🤖 Loading ML model...")
    if not load_model():
        print("\n❌ Failed to load model!")
        print("Please run: python train_model.py")
        exit(1)
    
    # Run Flask app
    print("\n🌐 Starting Flask server...")
    print("   Open: http://localhost:5000")
    print("   Press Ctrl+C to stop\n")
    
    # Enable debug mode for development (disable in production)
    app.run(debug=True, host='0.0.0.0', port=5000)

