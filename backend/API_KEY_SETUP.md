# 🔑 Gemini API Key Setup Guide

## Why You Need This

The app uses Google Gemini AI to:
- ✅ Generate realistic product catalogs
- ✅ Create smart, context-aware recommendations
- ✅ Power the chatbot explanations

**Without the API key:** The app will work but use basic fallback logic instead of AI.

## Get Your Free Gemini API Key

### Step 1: Visit Google AI Studio
Go to: **https://makersuite.google.com/app/apikey**

### Step 2: Sign In
- Use your Google account
- Accept terms if prompted

### Step 3: Create API Key
1. Click **"Create API Key"**
2. Select **"Create API key in new project"** (or use existing)
3. Copy the key (starts with `AIza...`)

### Step 4: Add to Your Project

1. **Open file:** `backend\.env`
2. **Replace the placeholder:**

```env
# Before:
GEMINI_API_KEY=your_gemini_api_key_here

# After (example):
GEMINI_API_KEY=AIzaSyABCDEFGHIJKLMNOPQRSTUVWXYZ1234567
```

3. **Save the file**

### Step 5: Restart Backend

```powershell
# Stop the backend (Ctrl+C in the terminal)
# Then restart:
cd backend
.\venv\Scripts\Activate.ps1
uvicorn main:app --reload
```

## Verify It's Working

### Test 1: Generate Products
1. Open http://localhost:5173
2. Click "Generate Products"
3. If successful, you'll see AI-generated products!

### Test 2: Check Recommendations
1. Add items to cart (e.g., Banana, Milk, Bread)
2. Smart recommendations should appear
3. Click "Why?" to see AI explanations

### Test 3: Use Chatbot
1. Click "💬 Ask AI"
2. Ask: "Why was this recommended?"
3. You should get a detailed AI response

## Troubleshooting

### Error: "API key not found"
- ✅ Check `.env` file exists in `backend` folder
- ✅ No spaces around `=` sign
- ✅ No quotes around the key
- ✅ Restart backend server

### Error: "Failed to generate products"
- ✅ Verify API key is correct (starts with `AIza`)
- ✅ Check internet connection
- ✅ Try with fewer products (20-30)
- ✅ Check API quota at Google AI Studio

### Still Getting "Popular item you might like"?
This means the fallback logic is being used. Reasons:
- ❌ API key not configured
- ❌ Gemini API error
- ❌ Network issue

**Solution:** Follow steps above and restart backend.

## Current Status

### ✅ With Gemini API Key:
- Smart AI-generated products
- Context-aware recommendations
- "Perfect pairing! Fresh bakery items pair excellently..."
- Interactive chatbot

### ⚠️ Without API Key (Fallback):
- Basic product catalog
- Category-based recommendations  
- "Great addition! This item complements your selection..."
- Limited chatbot

## Free Tier Limits

Gemini API free tier includes:
- **60 requests per minute**
- **1,500 requests per day**

More than enough for this project!

## Security Note

**Never commit your API key to Git!**

The `.env` file is already in `.gitignore` to protect your key.

---

**Need help?** Check the backend terminal for error messages!
