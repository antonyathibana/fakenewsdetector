# Fake News Detection Web Application

A production-ready web application that uses Machine Learning to detect fake news articles. Built with Python, Flask, and Scikit-learn.

![Python](https://img.shields.io/badge/Python-3.8+-blue)
![Flask](https://img.shields.io/badge/Flask-3.0-orange)
![License](https://img.shields.io/badge/License-MIT-green)

## 📋 Features

- **Text Analysis**: Analyze news articles to determine if they're fake or real
- **URL Analysis**: Optional bonus feature to check news from URLs
- **History Tracking**: SQLite database stores all predictions
- **Responsive UI**: Modern Bootstrap-based interface
- **Model Accuracy**: ~90%+ accuracy with Logistic Regression

## 🏗️ Project Structure

```
FAKE_NEWS_DETECTION/
├── app.py                    # Main Flask application
├── config.py                 # Configuration settings
├── database.py               # SQLite database module
├── preprocess_data.py        # Data preprocessing
├── train_model.py           # Model training script
├── requirements.txt         # Python dependencies
├── model.pkl      # Trained ML model (generated)
├── vectorizer.pkl     # TF-IDF vectorizer (generated)
├── news_history.db          # SQLite database (generated)
├── templates/                # HTML templates
│   ├── base.html
│   ├── index.html
│   ├── result.html
│   ├── history.html
│   ├── view_prediction.html
│   └── error.html
├── static/                   # CSS and JS files
│   ├── css/style.css
│   └── js/main.js
├── data/                     # Dataset files
│   ├── Fake.csv
│   └── True.csv
└── README.md
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Installation Steps

1. **Clone or download the project**

2. **Create virtual environment (recommended)**
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Download the datasets**
   
   Download the Fake and Real News dataset from Kaggle:
   - URL: https://www.kaggle.com/datasets/clmentbisaillon/fake-and-real-news-dataset
   
   Place the files in the `data/` folder:
   - `data/Fake.csv`
   - `data/True.csv`

5. **Train the model**
   ```bash
   python train_model.py
   ```
   
   This will:
   - Load and preprocess the datasets
   - Train a Logistic Regression model
   - Save `model.pkl` and `vectorizer.pkl`
   - Show model accuracy (typically ~90%+)

6. **Run the application**
   ```bash
   python app.py
   ```

7. **Open your browser**
   
   Navigate to: http://localhost:5000

## 📖 Usage

### Using the Web Interface

1. Open http://localhost:5000
2. Choose input type: Text or URL
3. Enter the news text or URL
4. Click "Analyze News"
5. View the prediction result with confidence score

### View History

Navigate to http://localhost:5000/history to see all past predictions.

## 🔧 Configuration

Edit `config.py` to customize:

```python
# Maximum features for TF-IDF
MAX_FEATURES = 10000

# N-gram range
NGRAM_RANGE = (1, 2)

# Items per page for history
ITEMS_PER_PAGE = 10
```

## ☁️ Deployment on Render

### Prerequisites
- GitHub account
- Render account (free tier works)

### Steps

1. **Push to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   # Create repository on GitHub and push
   ```

2. **Prepare for Render**
   
   Create a `build.sh` file:
   ```bash
   pip install -r requirements.txt
   python train_model.py
   ```

3. **Deploy on Render**
   - Log in to Render.com
   - Create new "Web Service"
   - Connect your GitHub repository
   - Set:
     - Build Command: `bash build.sh`
     - Start Command: `python app.py`
   - Click "Deploy"

4. **Environment Variables**
   
   Add in Render dashboard:
   - `SECRET_KEY`: Generate a secure random key
   - `DEBUG`: `false`

## 📊 Technical Details

### How It Works

1. **Data Preprocessing**
   - Text is converted to lowercase
   - Punctuation and numbers are removed
   - Stopwords (common words) are removed
   - URLs and email addresses are cleaned

2. **Feature Extraction**
   - TF-IDF (Term Frequency-Inverse Document Frequency) converts text to numerical features
   - Uses unigrams and bigrams (1-2 word combinations)
   - Maximum 10,000 features

3. **Model Training**
   - Logistic Regression classifier
   - Trained on labeled dataset (Fake=0, Real=1)
   - Achieves ~90%+ accuracy

4. **Prediction**
   - New text is preprocessed
   - Converted to TF-IDF features
   - Model predicts probability
   - Returns prediction with confidence

### System Architecture

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Client    │────▶│   Flask     │────▶│    ML       │
│  (Browser)  │◀────│   Server    │◀────│   Model     │
└─────────────┘     └─────────────┘     └─────────────┘
                           │
                           ▼
                    ┌─────────────┐
                    │  SQLite     │
                    │  Database   │
                    └─────────────┘
```

### ER Diagram

```
┌──────────────────┐
│   predictions    │
├──────────────────┤
│ id (PK)          │
│ text             │
│ prediction       │
│ confidence       │
│ is_url           │
│ created_at       │
└──────────────────┘
```

## 🎓 Viva Questions & Answers

### Q1: How does the fake news detection model work?

**Answer:** The model uses TF-IDF (Term Frequency-Inverse Document Frequency) vectorization to convert text into numerical features. Then, a Logistic Regression classifier is trained on labeled data (Fake=0, Real=1) to learn patterns that distinguish fake from real news. During prediction, the model analyzes the input text and outputs a probability score.

### Q2: Why did you choose Logistic Regression?

**Answer:** Logistic Regression was chosen because:
- It's simple and interpretable
- Works well with high-dimensional text data (TF-IDF)
- Provides probability outputs (confidence scores)
- Fast to train and predict
- Achieves ~90%+ accuracy on this dataset

### Q3: How do you handle URL-based predictions?

**Answer:** For URL input, we use BeautifulSoup to:
1. Fetch the webpage content
2. Remove script and style tags
3. Extract visible text content
4. Analyze the extracted text using the ML model

### Q4: What preprocessing steps are applied?

**Answer:**
- Lowercase conversion
- URL and email removal
- Punctuation removal
- Number removal
- Stopword removal
- Extra whitespace cleanup

### Q5: How is the model saved and loaded?

**Answer:** We use Python's `pickle` module to serialize:
- `model.pkl`: Trained Logistic Regression model
- `vectorizer.pkl`: Fitted TF-IDF vectorizer

These are loaded at application startup for fast predictions.

## 📝 License

MIT License - Feel free to use this project for learning or commercial purposes.

## 🙏 Acknowledgments

- Dataset: [Kaggle - Fake and Real News Dataset](https://www.kaggle.com/datasets/clmentbisaillon/fake-and-real-news-dataset)
- Built with Flask, Scikit-learn, and Bootstrap

