# Fake News Detection - Commands & Troubleshooting Guide

This document provides macOS commands to install pytest, run tests, and start the Flask application, along with troubleshooting solutions.

---

## 1. Install pytest

### Using pip3 (system-wide):
```bash
pip3 install pytest
```

### Using virtual environment (recommended):
```bash
cd "/Users/antonyadith/Desktop/FAKE NEWS DETECTION"
source venv/bin/activate
pip3 install pytest
```

### Verify installation:
```bash
pytest --version
# or
python3 -m pytest --version
```

---

## 2. Run test_app.py using python3

### Activate virtual environment first:
```bash
cd "/Users/antonyadith/Desktop/FAKE NEWS DETECTION"
source venv/bin/activate
```

### Run all tests:
```bash
python3 -m pytest test_app.py -v
```

### Run specific test class:
```bash
python3 -m pytest test_app.py::TestPreprocessData -v
python3 -m pytest test_app.py::TestDatabase -v
python3 -m pytest test_app.py::TestFlaskApp -v
```

### Run with detailed output:
```bash
python3 -m pytest test_app.py -v --tb=short
```

---

## 3. Start Flask Application

### First, ensure dependencies are installed:
```bash
pip3 install -r requirements.txt
```

### Then start the Flask app:
```bash
python3 app.py
```

### Alternative - Run Flask directly:
```bash
python3 -m flask run
```

### Run on specific port:
```bash
python3 app.py
# Or modify config.py PORT variable, or use:
FLASK_PORT=8080 python3 app.py
```

---

## 4. Troubleshooting

### Issue 1: pytest: command not found

**Problem:**
```
zsh: command not found: pytest
```

**Solutions:**

1. **Install pytest with pip3:**
   ```bash
   pip3 install pytest
   ```

2. **If already installed but not found, check PATH:**
   ```bash
   which pytest
   ```

3. **Use python3 -m pytest instead:**
   ```bash
   python3 -m pytest test_app.py -v
   ```

4. **Install pytest in user space (if permission issues):**
   ```bash
   pip3 install --user pytest
   ```

5. **Reinstall pytest with pip3:**
   ```bash
   pip3 uninstall pytest
   pip3 install pytest
   ```

6. **Check if pip3 is linked to correct Python:**
   ```bash
   pip3 --version
   python3 --version
   ```

---

### Issue 2: Model File Errors

**Problem:**
```
FileNotFoundError: [Errno 2] No such file or directory: 'model.pkl'
```

or

```
❌ Model files not found!
Please run: python train_model.py
```

**Solutions:**

1. **Check if model files exist:**
   ```bash
   ls -la *.pkl
   ```

2. **If model files don't exist, train the model:**
   ```bash
   python3 train_model.py
   ```

3. **Check config.py paths are correct:**
   The model expects files in the project root:
   - `model.pkl`
   - `vectorizer.pkl`

4. **If model loading fails with pickle error:**
   - The model may have been trained with a different Python version
   - Retrain the model:
     ```bash
     python3 train_model.py
     ```

5. **Manual check in Python:**
   ```bash
   python3 -c "import pickle; pickle.load(open('model.pkl', 'rb'))"
   ```

---

### Issue 3: Module Not Found Errors

**Problem:**
```
ModuleNotFoundError: No module named 'flask'
```

**Solution - Install all dependencies:**
```bash
pip3 install -r requirements.txt
```

**Individual package installation:**
```bash
pip3 install Flask>=3.0.0
pip3 install scikit-learn>=1.4.0
pip3 install pandas>=2.1.0
pip3 install nltk>=3.8.0
pip3 install beautifulsoup4>=4.12.0
pip3 install requests>=2.31.0
```

---

### Issue 4: NLTK Data Not Found

**Problem:**
```
LookupError: **************************************
    resource 'corpora/stopwords' not found
```

**Solution:**
```bash
python3 -c "import nltk; nltk.download('stopwords')"
python3 -c "import nltk; nltk.download('punkt')"
```

Or download all at once:
```bash
python3 -c "import nltk; nltk.download('stopwords'); nltk.download('punkt'); nltk.download('punkt_tab')"
```

---

### Issue 5: Database Permission Errors

**Problem:**
```
sqlite3.OperationalError: unable to open database file
```

**Solution:**
```bash
# Check current directory
pwd
# Should be: /Users/antonyadith/Desktop/FAKE NEWS DETECTION

# If database file has permission issues
touch news_history.db
chmod 666 news_history.db
```

---

### Issue 6: Port Already in Use

**Problem:**
```
OSError: [Errno 48] Address already in use
```

**Solution:**
```bash
# Find process using port 5000
lsof -i :5000

# Kill the process
kill -9 <PID>

# Or use a different port
# Edit config.py: PORT = 5001
```

---

## 5. Quick Reference Commands Summary

```bash
# Navigate to project directory
cd /Users/antonyadith/Desktop/FAKE\ NEWS\ DETECTION

# Install pytest
pip3 install pytest

# Run tests
python3 -m pytest test_app.py -v

# Install all dependencies
pip3 install -r requirements.txt

# Download NLTK data
python3 -c "import nltk; nltk.download('stopwords'); nltk.download('punkt'); nltk.download('punkt_tab')"

# Train model (if model files missing)
python3 train_model.py

# Start Flask application
python3 app.py
```

---

## 6. Expected Output

### Successful pytest run:
```
test_app.py::TestPreprocessData::test_preprocess_text_basic PASSED
test_app.py::TestPreprocessData::test_preprocess_text_empty PASSED
...
======================= X passed in X.XXs =======================
```

### Successful Flask startup:
```
==================================================
🚀 Fake News Detection Web Application
==================================================

📦 Initializing database...

🤖 Loading ML model...
✓ Model and vectorizer loaded successfully

🌐 Starting Flask server...
   Open: http://localhost:5000
   Press Ctrl+C to stop
```

