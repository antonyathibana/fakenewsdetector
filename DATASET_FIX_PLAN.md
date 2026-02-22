# Fake News Detection - Dataset Fix Plan

## Problem Identified:
- `data/Fake.csv` - Empty placeholder (14 bytes)
- `data/True.csv` - Empty placeholder (14 bytes)
- Error: "No 'text' or 'title' column found in dataset"

## Solution Plan:

### Option 1: Download from Kaggle (Recommended)
1. Download dataset from: https://www.kaggle.com/datasets/clmentbisaillon/fake-and-real-news-dataset
2. Extract and place files:
   - `data/Fake.csv`
   - `data/True.csv`

### Option 2: Create Sample Dataset (Quick Fix)
- Run `create_sample_data.py` to generate sample datasets
- This will create working CSV files for testing

### Step 3: Run Training
- Run `python train_model.py` to train the model

## Follow-up Steps:
1. Install dependencies: `pip install -r requirements.txt`
2. Create sample data: `python create_sample_data.py`
3. Train model: `python train_model.py`
4. Run app: `python app.py`

