# Deployment Fix Plan for Render

## Information Gathered:

### Current Project Structure:
- **Main app**: `app.py` - Flask application with ML model
- **Database**: SQLite (`news_history.db`)
- **Model files**: `model.pkl` and `vectorizer.pkl` (required)
- **Templates**: `/templates` folder
- **Static files**: `/static` folder

### Issues Identified:
1. **Python version issue**: `runtime.txt` specifies `python-3.14.2` - Python 3.14 is NOT available on Render yet
2. **Build timeout risk**: `build.sh` trains the model during build which may timeout on free tier
3. **Missing model files**: The app requires pre-trained model.pkl and vectorizer.pkl
4. **requirements.txt**: Has formatting issues

### Current Configuration Files:
- **Procfile**: `web: gunicorn app:app --workers 2 --bind 0.0.0.0:$PORT` ✅ (Correct)
- **render.yaml**: Uses Python 3.14 (needs fix)
- **build.sh**: Trains model during build (needs optimization)

## Plan:

### Step 1: Fix Python Version
- Update `runtime.txt` from `python-3.14.2` to `python-3.12.0`
- Update `render.yaml` pythonVersion from "3.14" to "3.12"

### Step 2: Fix requirements.txt
- Clean up formatting
- Add proper version pinning
- Remove duplicate sections

### Step 3: Optimize Build Process
- Modify `build.sh` to skip model training during build
- App will load pre-trained model files if they exist
- Add fallback message if model files are missing

### Step 4: Pre-train Model (Critical)
- Execute `train_model.py` locally to generate model.pkl and vectorizer.pkl
- These files must be committed to the repository for deployment

### Step 5: Update app.py for Production
- Ensure debug mode is disabled in production
- Add production-ready configurations

## Dependent Files to be Edited:
1. `runtime.txt` - Fix Python version
2. `render.yaml` - Fix Python version
3. `requirements.txt` - Fix formatting and add proper dependencies
4. `build.sh` - Optimize build process
5. Run `train_model.py` locally to generate model files

## Followup Steps:
1. Run `python train_model.py` locally to generate model.pkl and vectorizer.pkl
2. Commit all changes including generated model files
3. Deploy to Render using Python Web Service (not Docker)
4. Verify deployment works

## Render Settings Summary:
- **Environment**: Python (not Docker)
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn app:app --workers 2 --bind 0.0.0.0:$PORT`
- **Python Version**: 3.12

