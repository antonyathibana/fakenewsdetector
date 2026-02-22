"""
Configuration settings for Fake News Detection Web Application
"""

import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).parent

# Database configuration
DATABASE_PATH = BASE_DIR / 'news_history.db'

# Model paths
MODEL_PATH = BASE_DIR / 'model.pkl'
VECTORIZER_PATH = BASE_DIR / 'vectorizer.pkl'

# Data paths
FAKE_NEWS_PATH = BASE_DIR / 'data' / 'Fake.csv'
TRUE_NEWS_PATH = BASE_DIR / 'data' / 'True.csv'

# Flask configuration
SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'
PORT = int(os.environ.get('PORT', 5000))

# Model configuration
MAX_FEATURES = 10000
NGRAM_RANGE = (1, 2)

# Pagination
ITEMS_PER_PAGE = 10

# Google Fact Check API Configuration
# Get your API key from: https://developers.google.com/fact-check/tools-api
GOOGLE_FACT_CHECK_API_KEY = os.environ.get('GOOGLE_FACT_CHECK_API_KEY', '')
GOOGLE_FACT_CHECK_API_URL = 'https://factchecktools.googleapis.com/v1alpha1/claims:search'

