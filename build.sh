#!/bin/bash
# Build script for Render deployment
# This script runs during the build phase

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Training the model..."
python train_model.py

echo "Build complete!"

