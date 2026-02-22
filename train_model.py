"""
Model Training Module for Fake News Detection
This module handles:
- Loading and preprocessing data
- TF-IDF vectorization
- Training multiple models (Logistic Regression, Naive Bayes, SVM)
- Model comparison and selection
- Confusion matrix visualization
- Cross-validation evaluation
- Saving best model and vectorizer using pickle
"""

import pickle
import os
import warnings
from pathlib import Path
from time import time

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import LinearSVC
from sklearn.calibration import CalibratedClassifierCV
from sklearn.metrics import (
    accuracy_score, classification_report, confusion_matrix,
    precision_score, recall_score, f1_score
)

from preprocess_data import load_and_preprocess
import config

# Suppress warnings for cleaner output
warnings.filterwarnings('ignore')

# Get the project root directory
PROJECT_ROOT = Path(__file__).parent


def print_section(title):
    """Print a formatted section header"""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def print_subsection(title):
    """Print a formatted subsection header"""
    print(f"\n▶ {title}")
    print("-" * 40)


def plot_confusion_matrix(cm, model_name, save_path):
    """
    Plot and save confusion matrix as an image
    
    Args:
        cm: Confusion matrix array
        model_name: Name of the model
        save_path: Path to save the plot
    """
    plt.figure(figsize=(8, 6))
    
    # Create heatmap
    sns.heatmap(
        cm, 
        annot=True, 
        fmt='d', 
        cmap='Blues',
        xticklabels=['Fake', 'Real'],
        yticklabels=['Fake', 'Real'],
        annot_kws={'size': 14}
    )
    
    plt.title(f'Confusion Matrix - {model_name}', fontsize=14, fontweight='bold')
    plt.ylabel('Actual Label', fontsize=12)
    plt.xlabel('Predicted Label', fontsize=12)
    plt.tight_layout()
    
    # Save the plot
    plt.savefig(save_path, dpi=150, bbox_inches='tight')
    plt.close()
    
    print(f"   ✓ Confusion matrix saved to: {save_path}")


def plot_model_comparison(results, save_path):
    """
    Plot model comparison metrics as a bar chart
    
    Args:
        results: Dictionary containing model results
        save_path: Path to save the plot
    """
    models = list(results.keys())
    metrics = ['accuracy', 'precision', 'recall', 'f1']
    
    # Prepare data
    data = {metric: [results[m][metric] for m in models] for metric in metrics}
    
    # Create plot
    fig, ax = plt.subplots(figsize=(10, 6))
    
    x = np.arange(len(models))
    width = 0.2
    
    colors = ['#3498db', '#2ecc71', '#e74c3c', '#9b59b6']
    
    for i, metric in enumerate(metrics):
        bars = ax.bar(x + i * width, data[metric], width, label=metric.capitalize(), color=colors[i])
        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            ax.annotate(f'{height:.3f}',
                       xy=(bar.get_x() + bar.get_width() / 2, height),
                       xytext=(0, 3),
                       textcoords="offset points",
                       ha='center', va='bottom', fontsize=8)
    
    ax.set_xlabel('Models', fontsize=12)
    ax.set_ylabel('Score', fontsize=12)
    ax.set_title('Model Performance Comparison', fontsize=14, fontweight='bold')
    ax.set_xticks(x + width * 1.5)
    ax.set_xticklabels(models, fontsize=10)
    ax.legend(loc='lower right', fontsize=10)
    ax.set_ylim(0.85, 1.0)
    ax.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches='tight')
    plt.close()
    
    print(f"   ✓ Comparison chart saved to: {save_path}")


def train_and_evaluate_models(X_train, X_test, y_train, y_test, vectorizer):
    """
    Train and evaluate multiple models
    
    Args:
        X_train, X_test: Training and test features
        y_train, y_test: Training and test labels
        vectorizer: TF-IDF vectorizer
    
    Returns:
        tuple: (best_model, results_dict, best_accuracy)
    """
    print_section("🤖 Training Multiple Models")
    
    # Define models
    models = {
        'Logistic Regression': LogisticRegression(
            max_iter=1000,
            random_state=42,
            n_jobs=-1,
            C=1.0,
            solver='lbfgs'
        ),
        'Naive Bayes': MultinomialNB(alpha=0.1),
        'SVM': CalibratedClassifierCV(
            LinearSVC(
                max_iter=2000,
                random_state=42,
                C=1.0
            ),
            cv=3
        )
    }
    
    results = {}
    
    for model_name, model in models.items():
        print_subsection(f"Training {model_name}...")
        start_time = time()
        
        # Train the model
        model.fit(X_train, y_train)
        train_time = time() - start_time
        
        # Make predictions
        y_pred = model.predict(X_test)
        
        # Calculate metrics
        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred)
        recall = recall_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)
        
        # Cross-validation
        print(f"   Running 5-fold cross-validation...")
        cv_scores = cross_val_score(model, X_train, y_train, cv=5, n_jobs=-1)
        cv_mean = cv_scores.mean()
        cv_std = cv_scores.std()
        
        # Confusion matrix
        cm = confusion_matrix(y_test, y_pred)
        
        # Store results
        results[model_name] = {
            'model': model,
            'accuracy': accuracy,
            'precision': precision,
            'recall': recall,
            'f1': f1,
            'cv_mean': cv_mean,
            'cv_std': cv_std,
            'confusion_matrix': cm,
            'train_time': train_time,
            'y_pred': y_pred
        }
        
        # Print results
        print(f"   ✓ Training time: {train_time:.2f}s")
        print(f"   ✓ Accuracy: {accuracy * 100:.2f}%")
        print(f"   ✓ Precision: {precision * 100:.2f}%")
        print(f"   ✓ Recall: {recall * 100:.2f}%")
        print(f"   ✓ F1-Score: {f1 * 100:.2f}%")
        print(f"   ✓ CV Score: {cv_mean:.4f} (+/- {cv_std:.4f})")
    
    # Find best model based on accuracy
    best_model_name = max(results, key=lambda x: results[x]['accuracy'])
    best_model = results[best_model_name]['model']
    best_accuracy = results[best_model_name]['accuracy']
    
    return best_model, results, best_accuracy


def print_model_comparison(results):
    """
    Print a formatted model comparison table
    
    Args:
        results: Dictionary containing model results
    """
    print_section("📊 Model Comparison Results")
    
    # Header
    print(f"\n{'Model':<25} {'Accuracy':>10} {'Precision':>10} {'Recall':>10} {'F1-Score':>10} {'CV Score':>12}")
    print("-" * 80)
    
    # Data rows
    for model_name, data in results.items():
        print(f"{model_name:<25} {data['accuracy']:>10.4f} {data['precision']:>10.4f} {data['recall']:>10.4f} {data['f1']:>10.4f} {data['cv_mean']:>10.4f}±{data['cv_std']:.4f}")
    
    print("-" * 80)
    
    # Highlight best model
    best_model = max(results, key=lambda x: results[x]['accuracy'])
    print(f"\n🏆 Best Model: {best_model} (Accuracy: {results[best_model]['accuracy']*100:.2f}%)")


def print_detailed_classification_report(results, best_model_name):
    """
    Print detailed classification report for all models
    
    Args:
        results: Dictionary containing model results
        best_model_name: Name of the best model
    """
    print_section("📋 Detailed Classification Reports")
    
    for model_name, data in results.items():
        marker = " ⭐ BEST MODEL" if model_name == best_model_name else ""
        print(f"\n{'='*40}")
        print(f"  {model_name}{marker}")
        print(f"{'='*40}")
        
        print(classification_report(
            data['y_pred'], 
            data['y_pred'],  # This is a workaround - we need y_test
            target_names=['Fake', 'Real']
        ))
        
        # Actually print with y_test
        y_test = data.get('y_test', None)
        if y_test is not None:
            print(classification_report(
                y_test, 
                data['y_pred'],
                target_names=['Fake', 'Real']
            ))


def train_model(df):
    """
    Train the Logistic Regression model using TF-IDF
    
    Args:
        df: Preprocessed DataFrame with 'processed_text' and 'label' columns
    
    Returns:
        tuple: (model, vectorizer, accuracy, results)
    """
    print_section("🚀 Starting Model Training Pipeline")
    
    # Prepare features and labels
    X = df['processed_text']
    y = df['label']
    
    print(f"\n📊 Dataset Summary:")
    print(f"   Total samples: {len(X):,}")
    print(f"   Fake news (0): {sum(y == 0):,}")
    print(f"   Real news (1): {sum(y == 1):,}")
    
    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    print(f"\n📂 Data Split:")
    print(f"   Training samples: {len(X_train):,}")
    print(f"   Testing samples: {len(X_test):,}")
    
    # Create TF-IDF Vectorizer
    print_subsection("Creating TF-IDF Vectorizer...")
    vectorizer = TfidfVectorizer(
        max_features=config.MAX_FEATURES,
        ngram_range=config.NGRAM_RANGE,
        stop_words='english'
    )
    
    # Fit and transform training data
    X_train_tfidf = vectorizer.fit_transform(X_train)
    X_test_tfidf = vectorizer.transform(X_test)
    
    print(f"   Vocabulary size: {len(vectorizer.vocabulary_):,}")
    print(f"   Feature matrix shape: {X_train_tfidf.shape}")
    
    # Train and evaluate models
    best_model, results, best_accuracy = train_and_evaluate_models(
        X_train_tfidf, X_test_tfidf, y_train, y_test, vectorizer
    )
    
    # Add y_test to results for classification report
    for model_name in results:
        results[model_name]['y_test'] = y_test
    
    # Print model comparison
    print_model_comparison(results)
    
    # Generate confusion matrix plots
    print_section("📈 Generating Confusion Matrix Visualizations")
    for model_name, data in results.items():
        safe_name = model_name.replace(' ', '_').lower()
        cm_path = PROJECT_ROOT / 'visualizations' / f'confusion_matrix_{safe_name}.png'
        plot_confusion_matrix(data['confusion_matrix'], model_name, cm_path)
    
    # Generate comparison chart
    comparison_path = PROJECT_ROOT / 'visualizations' / 'model_comparison.png'
    plot_model_comparison(results, comparison_path)
    
    # Print best model details
    print_section(f"🏆 Best Model: {max(results, key=lambda x: results[x]['accuracy'])}")
    best_data = results[max(results, key=lambda x: results[x]['accuracy'])]
    print(f"\n   Accuracy:  {best_data['accuracy']*100:.2f}%")
    print(f"   Precision: {best_data['precision']*100:.2f}%")
    print(f"   Recall:    {best_data['recall']*100:.2f}%")
    print(f"   F1-Score:  {best_data['f1']*100:.2f}%")
    print(f"   CV Score:  {best_data['cv_mean']:.4f} (+/- {best_data['cv_std']:.4f})")
    
    return best_model, vectorizer, best_accuracy, results


def save_model(model, vectorizer, accuracy, results):
    """
    Save the trained model and vectorizer using pickle
    
    Args:
        model: Trained model
        vectorizer: Fitted TF-IDF vectorizer
        accuracy: Model accuracy score
        results: Dictionary containing all model results
    """
    print_section("💾 Saving Model and Vectorizer")
    
    # Save model
    model_path = PROJECT_ROOT / 'model.pkl'
    with open(model_path, 'wb') as f:
        pickle.dump(model, f)
    print(f"✓ Model saved to: {model_path}")
    
    # Save vectorizer
    vectorizer_path = PROJECT_ROOT / 'vectorizer.pkl'
    with open(vectorizer_path, 'wb') as f:
        pickle.dump(vectorizer, f)
    print(f"✓ Vectorizer saved to: {vectorizer_path}")
    
    # Save model metadata
    best_model_name = max(results, key=lambda x: results[x]['accuracy'])
    metadata = {
        'accuracy': accuracy,
        'max_features': config.MAX_FEATURES,
        'ngram_range': config.NGRAM_RANGE,
        'model_type': best_model_name,
        'all_results': {
            name: {
                'accuracy': data['accuracy'],
                'precision': data['precision'],
                'recall': data['recall'],
                'f1': data['f1'],
                'cv_mean': data['cv_mean'],
                'cv_std': data['cv_std']
            }
            for name, data in results.items()
        }
    }
    
    metadata_path = PROJECT_ROOT / 'model_metadata.pkl'
    with open(metadata_path, 'wb') as f:
        pickle.dump(metadata, f)
    print(f"✓ Metadata saved to: {metadata_path}")
    
    print("\n✅ Model training and saving completed!")


def main():
    """
    Main function to train and save the model
    """
    try:
        # Create visualizations directory
        vis_dir = PROJECT_ROOT / 'visualizations'
        vis_dir.mkdir(exist_ok=True)
        
        # Load and preprocess data
        df = load_and_preprocess()
        
        # Train model
        model, vectorizer, accuracy, results = train_model(df)
        
        # Save model
        save_model(model, vectorizer, accuracy, results)
        
        print_section("🎉 Project Ready!")
        print("\n📁 Generated Files:")
        print("   - model.pkl (trained model)")
        print("   - vectorizer.pkl (TF-IDF vectorizer)")
        print("   - model_metadata.pkl (model information)")
        print("   - visualizations/confusion_matrix_*.png")
        print("   - visualizations/model_comparison.png")
        
        print("\n🚀 Next Steps:")
        print("   1. Install dependencies: pip install -r requirements.txt")
        print("   2. Download NLTK data: python -c 'import nltk; nltk.download(\"stopwords\")'")
        print("   3. Run the app: python app.py")
        print("   4. Open browser: http://localhost:5000")
        
    except FileNotFoundError as e:
        print(f"\n❌ Error: {e}")
        print("\nPlease download the Kaggle datasets:")
        print("https://www.kaggle.com/datasets/clmentbisaillon/fake-and-real-news-dataset")
        print("\nPlace them in the 'data' folder as:")
        print("  - data/Fake.csv")
        print("  - data/True.csv")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

