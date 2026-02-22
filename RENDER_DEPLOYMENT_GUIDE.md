# RENDER DEPLOYMENT GUIDE
# Fake News Detection Flask Application

## ✅ All Fixes Applied

### Files Updated:
1. ✅ `runtime.txt` - Changed to python-3.12.0
2. ✅ `render.yaml` - Changed to Python 3.12, simplified build command
3. ✅ `requirements.txt` - Fixed formatting
4. ✅ `build.sh` - Removed model training (now uses pre-trained model)
5. ✅ `model.pkl` - Generated (12.6 KB)
6. ✅ `vectorizer.pkl` - Generated (61 KB)

---

## 🚀 RENDER SETTINGS (Use these exact values)

### In Render Dashboard:

| Setting | Value |
|---------|-------|
| **Environment** | Python |
| **Region** | Oregon (or your preference) |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `gunicorn app:app --workers 2 --bind 0.0.0.0:$PORT` |
| **Python Version** | 3.12 |
| **Plan** | Free |

### Environment Variables (Optional):
- `DEBUG`: false
- `SECRET_KEY`: (Leave empty - Render will generate one)

---

## 📋 ALTERNATIVE: Using render.yaml

The `render.yaml` file is already configured. You can connect your GitHub repository to Render and it will automatically use these settings.

```yaml
services:
  - type: web
    name: fakenewsdetector
    env: python
    region: oregon
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn app:app --workers 2 --bind 0.0.0.0:$PORT
    envVars:
      - key: DEBUG
        value: "false"
      - key: SECRET_KEY
        generateValue: true
    pythonVersion: "3.12"
    plan: free
```

---

## ⚠️ IMPORTANT NOTES

1. **DO NOT use Docker** - Use Python Web Service environment
2. **Model files are included** - model.pkl and vectorizer.pkl are now in the repo
3. **SQLite will work** - It's file-based, no additional setup needed
4. **Free tier limitations**:
   - Instance sleeps after 15 min of inactivity
   - 750 hours per month
   - 512 MB RAM

---

## 🔧 TROUBLESHOOTING

### If deployment fails:
1. Check that Python version is 3.12 (not 3.14)
2. Verify build command is exactly: `pip install -r requirements.txt`
3. Make sure model.pkl and vectorizer.pkl are committed to GitHub
4. Check Render build logs for specific errors

### If app crashes on startup:
- Verify all files are committed: `git add . && git commit -m "Deploy files"`
- Check that NLTK downloads work (build.sh handles this)
- Ensure database.py and config.py are present

---

## 📁 Files Ready for Deployment

```
FAKE NEWS DETECTION/
├── app.py                    # Main Flask app
├── config.py                 # Configuration
├── database.py              # SQLite database
├── model.pkl               # ✅ Trained model (generated)
├── vectorizer.pkl          # ✅ TF-IDF vectorizer (generated)
├── requirements.txt        # ✅ Fixed
├── runtime.txt             # ✅ Fixed to Python 3.12
├── render.yaml             # ✅ Fixed
├── build.sh                # ✅ Fixed (no training)
├── Procfile                # gunicorn config
├── templates/              # HTML templates
├── static/                 # CSS, JS, images
└── data/                   # Dataset files
```

---

## ✅ Deployment Checklist

- [x] Python version fixed to 3.12
- [x] requirements.txt formatted correctly
- [x] build.sh optimized (no training)
- [x] Model files generated (model.pkl, vectorizer.pkl)
- [x] render.yaml configured for Python
- [x] All files committed to GitHub

**Ready to deploy to Render!**

