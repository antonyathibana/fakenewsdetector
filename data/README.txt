# Data Files

This folder should contain the Kaggle Fake and Real News datasets.

## Download Instructions

1. Visit: https://www.kaggle.com/datasets/clmentbisaillon/fake-and-real-news-dataset

2. Download the dataset (you may need to sign in to Kaggle)

3. Extract the zip file

4. Copy the files to this folder:
   - Fake.csv → data/Fake.csv
   - True.csv → data/True.csv

## Dataset Format

Both CSV files should have columns like:
- title: News article title
- text: Full article text
- subject: Topic category
- date: Publication date

## Quick Download (Alternative)

If you have Kaggle CLI installed:
```bash
kaggle datasets download -d clmentbisaillon/fake-and-real-news-dataset
unzip fake-and-real-news-dataset.zip
mv Fake.csv True.csv data/
```

## Note

The datasets are not included in this repository due to size limits.
Please download them separately from Kaggle.

