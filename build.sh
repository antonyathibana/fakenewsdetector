#!/bin/bash
# Build script for Render deployment
# This script runs during the build phase

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Downloading NLTK data..."
python -c "import nltk; nltk.download('stopwords', quiet=True); nltk.download('punkt', quiet=True)"

echo "Build complete!"
echo ""
echo "NOTE: If model.pkl and vectorizer.pkl don't exist, please run train_model.py locally before deploying."
