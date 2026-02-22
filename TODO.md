# Fake News Detection Web Application - Project Plan

## 1. Project Overview
- **Project Name**: Fake News Detection Web Application
- **Type**: Full-stack Web Application with ML
- **Core Functionality**: Detect whether news articles are fake or real using Machine Learning
- **Target Users**: General public, journalists, researchers

## 2. Folder Structure
```
FAKE_NEWS_DETECTION/
├── app.py                      # Main Flask application ✅
├── config.py                   # Configuration settings ✅
├── requirements.txt            # Python dependencies ✅
├── train_model.py              # Model training script ✅
├── preprocess_data.py          # Data preprocessing script ✅
├── database.py                 # SQLite database module ✅
├── model.pkl         # Trained ML model (to be generated)
├── vectorizer.pkl        # TF-IDF vectorizer (to be generated)
├── news_history.db             # SQLite database (auto-generated)
├── templates/
│   ├── base.html              # Base template ✅
│   ├── index.html             # Home page ✅
│   ├── result.html            # Result page ✅
│   ├── history.html           # History page ✅
│   ├── view_prediction.html   # View prediction ✅
│   └── error.html             # Error page ✅
├── static/
│   ├── css/
│   │   └── style.css          # Custom styles ✅
│   └── js/
│       └── main.js            # JavaScript ✅
├── data/
│   ├── Fake.csv               # Fake news dataset (to download)
│   ├── True.csv               # Real news dataset (to download)
│   └── README.txt             # Dataset instructions ✅
├── README.md                   # Setup instructions ✅
└── .gitignore                 # Git ignore ✅
```

## 3. Implementation Status

### Phase 1: Data & ML Pipeline ✅
- [x] Create requirements.txt
- [ ] Download Kaggle datasets (Fake.csv, True.csv) - **User needs to do this**
- [x] Create preprocess_data.py for data cleaning
- [x] Create train_model.py for model training

### Phase 2: Backend (Flask) ✅
- [x] Create config.py for configuration
- [x] Create app.py with routes:
  - "/" → Home page ✅
  - "/predict" → POST prediction ✅
  - "/history" → View prediction history ✅

### Phase 3: Frontend ✅
- [x] Create base.html template
- [x] Create index.html with form
- [x] Create result.html for display
- [x] Create history.html
- [x] Create view_prediction.html
- [x] Create error.html
- [x] Create style.css for styling
- [x] Create main.js for interactivity

### Phase 4: Database & Extras ✅
- [x] Implement SQLite history storage
- [x] Add URL-based prediction (bonus)
- [x] Add error handling
- [x] Write README.md with full documentation

### Phase 5: Documentation ✅
- [x] System architecture diagram description (in README.md)
- [x] ER diagram description (in README.md)
- [x] Technical explanation for viva (in README.md)
- [x] Deployment steps for Render (in README.md)

## 4. Technical Stack
- **Backend**: Python 3.x, Flask
- **ML**: Scikit-learn (Logistic Regression, TF-IDF)
- **Database**: SQLite
- **Frontend**: HTML5, CSS3, Bootstrap 5, JavaScript

## 5. Expected Outcomes
- Model accuracy: ~90%+
- Responsive UI
- History tracking
- Production-ready code

## 6. Next Steps (User Actions Required)

1. **Download Dataset**:
   - Go to: https://www.kaggle.com/datasets/clmentbisaillon/fake-and-real-news-dataset
   - Download Fake.csv and True.csv
   - Place in `data/` folder

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Train Model**:
   ```bash
   python train_model.py
   ```

4. **Run Application**:
   ```bash
   python app.py
   ```

5. **Open Browser**:
   - Go to: http://localhost:5000

---

## 7. Deployment (Render)

The app is ready for deployment. See README.md for detailed deployment steps.

### Quick Deploy:
1. Push to GitHub
2. Create Web Service on Render
3. Connect repo
4. Set Build Command: `pip install -r requirements.txt`
5. Set Start Command: `python app.py`

