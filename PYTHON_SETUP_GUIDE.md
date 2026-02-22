# Fake News Detection - Python Environment Setup Guide

This guide provides step-by-step instructions to fix Pylance "import could not be resolved" errors for `bs4`, `requests`, and `sklearn` modules.

---

## 1. Virtual Environment Setup (Recommended)

### Step 1.1: Create a Virtual Environment

```bash
cd "/Users/antonyadith/Desktop/FAKE NEWS DXETECTION"
```

```bash
python3 -m venv venv
```

### Step 1.2: Activate the Virtual Environment

```bash
# On macOS/Linux:
source venv/bin/activate

# On Windows (if needed):
# venv\Scripts\activate
```

### Step 1.3: Upgrade pip

```bash
pip install --upgrade pip
```

### Step 1.4: Install All Dependencies

```bash
pip install -r requirements.txt
```

Or install individually:

```bash
pip install Flask==3.0.0 Werkzeug==3.0.1
pip install scikit-learn==1.3.2 numpy==1.26.2 pandas==2.1.4
pip install beautifulsoup4==4.12.2 lxml==4.9.3 requests==2.31.0
pip install python-dotenv==1.0.0
```

---

## 2. VS Code Interpreter Selection Steps

### Step 2.1: Open Command Palette

- Press `Cmd + Shift + P` (macOS) or `Ctrl + Shift + P` (Windows/Linux)

### Step 2.2: Select Python Interpreter

1. Type: `Python: Select Interpreter`
2. Press `Enter`
3. Look for interpreter path starting with `./venv/bin/python` or similar
4. Select it

**Expected interpreter path:**
```
/Users/antonyadith/Desktop/FAKE NEWS DXETECTION/venv/bin/python
```

> **⚠️ Important Note:** If you don't see the venv interpreter, make sure the virtual environment was created with Python 3.12 (use `/opt/homebrew/bin/python3.12 -m venv venv`). Python 3.14 is NOT compatible with scikit-learn 1.3.2 - you must use Python 3.11 or 3.12.

### Step 2.3: Verify Pylance is Using Correct Interpreter

1. Press `Cmd + Shift + P`
2. Type: `Python: Restart Language Server`
3. Select and restart

---

## 3. Exact Shell Commands (One-Line Summary)

Run these commands in sequence:

```bash
cd "/Users/antonyadith/Desktop/FAKE NEWS DXETECTION" && /opt/homebrew/bin/python3.12 -m venv venv && source venv/bin/activate && pip install --upgrade pip && pip install -r requirements.txt
```

Or step by step:

```bash
# Step 1: Create virtual environment with Python 3.12
/opt/homebrew/bin/python3.12 -m venv venv

# Step 2: Activate the virtual environment
source venv/bin/activate

# Step 3: Upgrade pip
pip install --upgrade pip

# Step 4: Install all dependencies
pip install -r requirements.txt
```

---

## 4. Verify Installation

### Check if packages are installed:

```bash
pip list | grep -E "Flask|sklearn|beautifulsoup4|requests|numpy|pandas"
```

### Test imports in Python:

```bash
python -c "from bs4 import BeautifulSoup; print('✓ bs4 OK')"
python -c "import requests; print('✓ requests OK')"
python -c "from sklearn.model_selection import train_test_split; print('✓ sklearn OK')"
python -c "import flask; print('✓ Flask OK')"
```

---

## 5. Troubleshooting Checklist

### ❌ Issue: "python: command not found"

**Solution:** Use `python3` instead of `python`

```bash
python3 --version
python3 -m venv venv
```

---

### ❌ Issue: "No module named 'pip'"

**Solution:** Install pip first

```bash
python3 -m ensurepip --upgrade
# OR
python3 -m pip install --upgrade pip
```

---

### ❌ Issue: VS Code still shows import errors

**Solution Steps:**

1. **Check current interpreter:**
   - `Cmd + Shift + P` → `Python: Select Interpreter`
   - Ensure it shows `./venv/bin/python`

2. **Reload VS Code Window:**
   - `Cmd + Shift + P` → `Developer: Reload Window`

3. **Check Pylance settings:**
   - Go to `Code → Settings → Extensions → Python`
   - Ensure "Pylance" is enabled
   - Check "Python: Analysis > Extra Paths" is empty or correct

---

### ❌ Issue: "ModuleNotFoundError" when running app

**Solution:** Ensure virtual environment is activated

```bash
# Always activate before running:
source venv/bin/activate
python app.py
```

---

### ❌ Issue: Multiple Python versions installed

**Solution:** Check which Python is being used

```bash
which python3
which pip3
which -a python3
```

Select the correct one in VS Code (see Step 2.2)

---

### ❌ Issue: requirements.txt not found

**Solution:** Use full path

```bash
pip install -r "/Users/antonyadith/Desktop/FAKE NEWS DXETECTION/requirements.txt"
```

---

## 6. Production-Ready Setup (Alternative)

If you prefer a system-wide installation (not recommended):

```bash
# Install Homebrew (macOS)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python
brew install python

# Install packages
pip3 install Flask==3.0.0 Werkzeug==3.0.1 scikit-learn==1.3.2 numpy==1.26.2 pandas==2.1.4 beautifulsoup4==4.12.2 lxml==4.9.3 requests==2.31.0 python-dotenv==1.0.0
```

---

## 7. Quick Fix Commands Summary

| Task | Command |
|------|---------|
| Create venv | `python3 -m venv venv` |
| Activate venv | `source venv/bin/activate` |
| Install deps | `pip install -r requirements.txt` |
| Run app | `python app.py` |
| Deactivate venv | `deactivate` |
| Delete venv | `rm -rf venv` |

---

## 8. Expected Output After Fix

When you run `python app.py`, you should see:

```
==================================================
🚀 Fake News Detection Web Application
==================================================

📦 Initializing database...
✓ Database initialized

🤖 Loading ML model...
✓ Model and vectorizer loaded successfully

🌐 Starting Flask server...
   Open: http://localhost:5000
   Press Ctrl+C to stop
```

---

## Notes

- **Always activate** the virtual environment before working on the project
- **Never commit** `venv/` folder to version control (already in `.gitignore`)
- **Use `pip`** (not pip3) after activating venv
- **Restart Pylance** if imports still show errors after setup

---

*Last updated: 2024*

