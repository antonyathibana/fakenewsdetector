"""
Data Preprocessing Module for Fake News Detection
This module handles:
- Loading datasets (Fake.csv and True.csv)
- Combining datasets with proper labels
- Text preprocessing (lowercasing, removing punctuation, stopwords, stemming)
"""

import pandas as pd
import re
import string
import os
from pathlib import Path

# Try to import NLTK for stemming, use fallback if not available
try:
    import nltk
    from nltk.stem import PorterStemmer
    nltk_available = True
except ImportError:
    nltk_available = False
    print("Warning: NLTK not available. Using simple stemming.")

# Get the project root directory
PROJECT_ROOT = Path(__file__).parent

# Initialize Porter Stemmer (or use simple fallback)
if nltk_available:
    stemmer = PorterStemmer()
else:
    # Simple suffix-stripping stemmer fallback
    class SimpleStemmer:
        def __init__(self):
            self.suffixes = ('ing', 'ed', 'ness', 'ly', 'ment', 'tion', 'sion', 'ity', 'ful', 'able', 'ible')
        
        def stem(self, word):
            word = word.lower()
            for suffix in self.suffixes:
                if word.endswith(suffix) and len(word) > len(suffix) + 2:
                    return word[:-len(suffix)]
            return word
    
    stemmer = SimpleStemmer()

# Built-in English stopwords (no download required)
STOPWORDS = {
    'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 
    "you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 
    'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 
    'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 
    'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 
    'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 
    'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 
    'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 
    'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 
    'by', 'for', 'with', 'about', 'against', 'between', 'into', 
    'through', 'during', 'before', 'after', 'above', 'below', 'to', 
    'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 
    'again', 'further', 'then', 'once', 'here', 'there', 'when', 
    'where', 'why', 'how', 'all', 'each', 'few', 'more', 'most', 
    'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 
    'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 
    'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll', 
    'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', 
    "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 
    'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 
    'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 
    'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 
    'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't", 
    'also', 'would', 'could', 'said', 'one', 'two', 'like', 'get', 
    'go', 'goes', 'went', 'come', 'came', 'make', 'made', 'know', 
    'knew', 'see', 'saw', 'think', 'thought', 'want', 'use', 'used'
}


def load_datasets():
    """
    Load fake and real news datasets from CSV files
    
    Returns:
        tuple: (fake_df, true_df)
    """
    fake_path = PROJECT_ROOT / 'data' / 'Fake.csv'
    true_path = PROJECT_ROOT / 'data' / 'True.csv'
    
    # Check if datasets exist
    if not fake_path.exists() or not true_path.exists():
        raise FileNotFoundError(
            f"Datasets not found! Please download:\n"
            f"- {fake_path}\n"
            f"- {true_path}\n"
            f"Get them from: https://www.kaggle.com/datasets/clmentbisaillon/fake-and-real-news-dataset"
        )
    
    # Load datasets
    fake_df = pd.read_csv(fake_path)
    true_df = pd.read_csv(true_path)
    
    print(f"✓ Loaded Fake news dataset: {len(fake_df)} articles")
    print(f"✓ Loaded True news dataset: {len(true_df)} articles")
    
    return fake_df, true_df


def add_labels(fake_df, true_df):
    """
    Add labels to datasets:
    - Fake = 0
    - Real = 1
    
    Args:
        fake_df: DataFrame with fake news
        true_df: DataFrame with real news
    
    Returns:
        DataFrame: Combined dataset with labels
    """
    # Add labels
    fake_df['label'] = 0  # Fake = 0
    true_df['label'] = 1  # Real = 1
    
    # Combine datasets
    df = pd.concat([fake_df, true_df], ignore_index=True)
    
    print(f"✓ Combined dataset: {len(df)} articles")
    print(f"  - Fake news: {len(fake_df)}")
    print(f"  - Real news: {len(true_df)}")
    
    return df


def preprocess_text(text):
    """
    Preprocess text by:
    1. Converting to lowercase
    2. Removing URLs and emails
    3. Removing punctuation
    4. Removing numbers
    5. Removing stopwords
    6. Applying Porter Stemming
    
    Args:
        text: Input text string
    
    Returns:
        str: Preprocessed text
    """
    if pd.isna(text):
        return ""
    
    # Convert to string
    text = str(text)
    
    # Convert to lowercase
    text = text.lower()
    
    # Remove URLs
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
    
    # Remove email addresses
    text = re.sub(r'\S+@\S+', '', text)
    
    # Remove punctuation
    text = text.translate(str.maketrans('', '', string.punctuation))
    
    # Remove numbers
    text = re.sub(r'\d+', '', text)
    
    # Remove extra whitespace
    text = ' '.join(text.split())
    
    # Remove stopwords and apply stemming
    words = text.split()
    # First remove stopwords, then apply stemming to remaining words
    words = [stemmer.stem(word) for word in words if word not in STOPWORDS]
    
    return ' '.join(words)


def preprocess_dataset(df):
    """
    Preprocess the entire dataset
    
    Args:
        df: DataFrame with 'text' column
    
    Returns:
        DataFrame: Preprocessed dataset
    """
    print("\n📝 Preprocessing text data...")
    
    # Check if 'text' column exists
    if 'text' not in df.columns:
        # Try 'Title' column
        if 'title' in df.columns:
            df['text'] = df['title'] + ' ' + df.get('subject', '')
        else:
            raise ValueError("No 'text' or 'title' column found in dataset")
    
    # Apply preprocessing to text column
    df['processed_text'] = df['text'].apply(preprocess_text)
    
    print("✓ Text preprocessing completed")
    
    return df


def load_and_preprocess():
    """
    Main function to load and preprocess data
    
    Returns:
        DataFrame: Preprocessed and labeled dataset
    """
    print("=" * 50)
    print("📊 Loading and Preprocessing Data")
    print("=" * 50)
    
    # Load datasets
    fake_df, true_df = load_datasets()
    
    # Add labels
    df = add_labels(fake_df, true_df)
    
    # Preprocess
    df = preprocess_dataset(df)
    
    print("\n✅ Data preprocessing completed!")
    print("=" * 50)
    
    return df


if __name__ == "__main__":
    # Test the preprocessing
    df = load_and_preprocess()
    print(f"\nDataset shape: {df.shape}")
    print(f"\nSample processed text:")
    print(df['processed_text'].iloc[0][:200])

