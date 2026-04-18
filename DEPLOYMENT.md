# 🎬 Bengali Movie Review Generator - Deployment Guide

## 🚀 Quick Deploy to Streamlit Cloud

### Prerequisites
1. GitHub account
2. Google Gemini API key

### Step 1: Push to GitHub

```bash
cd 04_Phase4_WebInterface
git init
git add .
git commit -m "Initial deployment"
git branch -M main
git remote add origin YOUR_GITHUB_REPO_URL
git push -u origin main
```

### Step 2: Deploy on Streamlit Cloud

1. Go to https://share.streamlit.io/
2. Sign in with GitHub
3. Click "New app"
4. Select your repository
5. Set:
   - **Main file path:** `streamlit_app/Home.py`
   - **Python version:** 3.10
6. Click "Advanced settings"
7. Add secrets:
   ```toml
   GOOGLE_API_KEY = "your_api_key_here"
   ```
8. Click "Deploy"

### Step 3: Wait for Deployment

- First deployment takes 5-10 minutes
- App will auto-update on git push

### Step 4: Access Your App

Your app will be available at:
```
https://your-app-name.streamlit.app
```

---

## 📦 Required Files

✅ `requirements.txt` - Python dependencies
✅ `.streamlit/config.toml` - Streamlit configuration
✅ `.env.template` - API key template
✅ `streamlit_app/Home.py` - Main entry point

---

## 🔑 Environment Variables

Add these in Streamlit Cloud secrets:

```toml
GOOGLE_API_KEY = "your_google_gemini_api_key"
```

---

## 📊 Database

- SQLite database will be created automatically
- Data persists across sessions
- Backup database file regularly

---

## 🛠️ Troubleshooting

### Issue: Module not found
**Solution:** Check `requirements.txt` has all dependencies

### Issue: API key error
**Solution:** Add `GOOGLE_API_KEY` in Streamlit secrets

### Issue: ChromaDB error
**Solution:** ChromaDB will initialize on first run

### Issue: Model loading slow
**Solution:** First load takes time, subsequent loads are cached

---

## 🔄 Update Deployment

```bash
git add .
git commit -m "Update message"
git push
```

Streamlit Cloud auto-deploys on push!

---

## 📈 Monitor Usage

- Check Streamlit Cloud dashboard
- Monitor API quota (20 requests/day free tier)
- Check database size

---

## 🎯 Production Checklist

- [ ] API key added to secrets
- [ ] Requirements.txt updated
- [ ] Database backup strategy
- [ ] Error handling tested
- [ ] Mobile responsive checked
- [ ] API quota monitored

---

## 🌐 Custom Domain (Optional)

1. Go to Streamlit Cloud settings
2. Add custom domain
3. Update DNS records
4. Wait for SSL certificate

---

## 💾 Backup Strategy

```bash
# Backup database
cp streamlit_app/movie_reviews.db backups/movie_reviews_$(date +%Y%m%d).db

# Backup ChromaDB
cp -r streamlit_app/chroma_db backups/chroma_db_$(date +%Y%m%d)
```

---

## 📞 Support

- Streamlit Docs: https://docs.streamlit.io/
- Community Forum: https://discuss.streamlit.io/
- GitHub Issues: Your repo issues page

---

**Last Updated:** 2025-01-XX
**Status:** Ready for Deployment ✅
