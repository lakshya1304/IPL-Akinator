# 🚀 Render Deployment Guide - IPL Akinator Backend

## Issues Fixed ✅

### 1. **Hardcoded API Keys** ❌→✅

- **Problem**: API keys were hardcoded as literal strings
- **Files Fixed**:
  - `engine/gemini_reasoner.py`
  - `engine/advanced_reasoner.py`
  - `engine/question_generator.py`
- **Solution**: Now uses `os.getenv("GEMINI_API_KEY")` with environment variable validation

### 2. **Missing Import** ❌→✅

- **Problem**: `question_generator.py` used undefined `client`
- **Solution**: Added proper imports and client initialization at module level

### 3. **Python Version** ❌→✅

- **Problem**: Python 3.13 has limited support on Render
- **Solution**: Updated `runtime.txt` to `python-3.11.0` (stable, widely supported)

### 4. **Missing Dependency** ❌→✅

- **Problem**: No `python-dotenv` for environment variable loading
- **Solution**: Added to `requirements.txt`

### 5. **Relative File Paths** ❌→✅

- **Problem**: Hardcoded relative paths broke when working directory changed
- **Files Fixed**:
  - `api.py` - Uses `Path(__file__).resolve().parent` for absolute paths
  - `engine/feedback_learner.py` - Uses absolute paths with directory creation
- **Solution**: All file paths are now absolute and robust

---

## 📋 Deployment Checklist for Render

### Step 1: Set Environment Variables on Render

1. Go to your Render dashboard
2. Select your service → Settings → Environment
3. Add variable:
   ```
   GEMINI_API_KEY = your_actual_api_key_here
   ```

### Step 2: Verify Files

The following files have been created/updated:

- ✅ `runtime.txt` - Python 3.11
- ✅ `requirements.txt` - Added python-dotenv==1.0.0
- ✅ `Procfile` - Render startup command
- ✅ `.env.example` - Reference for environment variables
- ✅ `api.py` - Fixed file paths and env loading
- ✅ `engine/gemini_reasoner.py` - Fixed API key handling
- ✅ `engine/advanced_reasoner.py` - Fixed API key handling
- ✅ `engine/question_generator.py` - Fixed imports and API key handling
- ✅ `engine/feedback_learner.py` - Fixed file paths

### Step 3: Deploy

Push changes to GitHub:

```bash
git add .
git commit -m "Fix: Render deployment issues - API keys, paths, and dependencies"
git push
```

Render will automatically redeploy from your connected GitHub repo.

### Step 4: Verify Deployment

1. Check Render Logs tab for errors
2. Test the API:
   ```bash
   curl https://your-render-url/
   curl https://your-render-url/start
   ```

---

## 🔧 Local Testing (Before Deployment)

```bash
cd backend

# Create .env file
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY

# Install dependencies
pip install -r requirements.txt

# Run locally
uvicorn api:app --reload
```

---

## 📝 File Summary

| File               | Change                   | Reason                        |
| ------------------ | ------------------------ | ----------------------------- |
| `runtime.txt`      | 3.13 → 3.11.0            | Better Render compatibility   |
| `requirements.txt` | +python-dotenv           | Environment variable support  |
| `Procfile`         | Created                  | Render deployment command     |
| `.env.example`     | Created                  | Documentation for env vars    |
| `api.py`           | Path fixes + env loading | Absolute paths, no hardcoding |
| `engine/*.py`      | API key → env vars       | Security & deployment ready   |

---

## ⚠️ Common Errors & Fixes

**Error**: `GEMINI_API_KEY environment variable not set`

- **Fix**: Add `GEMINI_API_KEY` to Render environment variables

**Error**: `FileNotFoundError: Players database not found`

- **Fix**: Ensure `database/` folder and JSON files are committed to Git

**Error**: `ModuleNotFoundError: No module named 'dotenv'`

- **Fix**: Ensure `pip install -r requirements.txt` runs during build

---

## ✨ Ready for Production!

Your backend is now deployment-ready. All security issues are fixed, and paths are absolute. Deploy with confidence! 🚀
