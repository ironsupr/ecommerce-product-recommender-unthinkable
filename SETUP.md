# E-Commerce Product Recommender - Setup Guide

## Quick Start (5 minutes)

### Step 1: Get Gemini API Key
1. Visit https://makersuite.google.com/app/apikey
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the key

### Step 2: Setup Backend
```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
# Edit .env and paste your API key
```

### Step 3: Setup Frontend
```bash
cd frontend
npm install
```

### Step 4: Run Application

Terminal 1 (Backend):
```bash
cd backend
venv\Scripts\activate
uvicorn main:app --reload
```

Terminal 2 (Frontend):
```bash
cd frontend
npm run dev
```

### Step 5: Initialize Data
1. Open http://localhost:5173
2. Click "Generate Products & Start Shopping"
3. Wait ~30 seconds for AI to create products
4. Start using the app!

## Troubleshooting

### "API Key not found"
- Make sure .env file exists in backend folder
- Verify GEMINI_API_KEY is set correctly
- No spaces around the = sign

### "Port already in use"
- Backend: Change port in uvicorn command: `uvicorn main:app --reload --port 8001`
- Frontend: Change port in vite.config.js

### "Failed to generate products"
- Check your internet connection
- Verify API key is valid
- Try reducing product count (start with 20)

### Database errors
- Delete ecommerce.db file and restart backend
- Run: `rm ecommerce.db` (Linux/Mac) or `del ecommerce.db` (Windows)

## API Documentation

Once backend is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Common Commands

```bash
# Reset database
cd backend
del ecommerce.db  # Windows
# rm ecommerce.db  # Linux/Mac

# Install new Python package
pip install <package-name>
pip freeze > requirements.txt

# Install new npm package
cd frontend
npm install <package-name>

# Build frontend for production
npm run build
```
