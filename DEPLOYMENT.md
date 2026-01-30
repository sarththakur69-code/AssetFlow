# WebScraper Deployment Guide

Complete step-by-step instructions for deploying AssetFlow to production.

---

##  Streamlit Cloud (Recommended - FREE)

**Best for:** Quick deployment, no server management, free hosting

### Steps:

1. **Push to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/yourusername/AssetFlow.git
   git push -u origin main
   ```

2. **Deploy on Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Click "New app"
   - Select your GitHub repo: `AssetFlow`
   - Main file path: `src/app.py`
   - Click "Deploy"

3. **Add API Key (Secrets)**
   - In Streamlit Cloud dashboard, click "⚙️ Settings"
   - Go to "Secrets"
   - Add:
     ```toml
     GEMINI_API_KEY = "your-api-key-here"
     ```
   - Save

**Done! Your app will be live at:** `https://your-app-name.streamlit.app`

---

##  Docker Deployment

**Best for:** Self-hosting, full control, containerization

### Dockerfile:

```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app files
COPY src/ ./src/
COPY .env .env

# Expose port
EXPOSE 8501

# Run app
CMD ["streamlit", "run", "src/app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### Build & Run:

```bash
# Build image
docker build -t assetflow .

# Run container
docker run -p 8501:8501 assetflow
```

**Access:** `http://localhost:8501`

---

##  Heroku Deployment

**Best for:** Scalable hosting, custom domains

### Prerequisites:
- Heroku CLI installed
- Heroku account

### Files Needed:

**Procfile:**
```
web: streamlit run src/app.py --server.port=$PORT --server.address=0.0.0.0
```

**runtime.txt:**
```
python-3.9.16
```

### Deploy:

```bash
# Login to Heroku
heroku login

# Create app
heroku create your-app-name

# Set API key
heroku config:set GEMINI_API_KEY=your-api-key-here

# Deploy
git push heroku main

# Open app
heroku open
```

---

##  Vercel/Netlify (NOT RECOMMENDED)

Streamlit apps don't work well on Vercel/Netlify. Use **Streamlit Cloud** or **Heroku** instead.

---

##  Security Best Practices

### 1. Environment Variables
- **Never commit `.env` files to Git**
- Add to `.gitignore`:
  ```
  .env
  assets/
  *.pdf
  *.csv
  ```

### 2. API Key Management
- Use platform secrets (Streamlit Cloud, Heroku Config Vars)
- Rotate keys regularly
- Monitor usage in Google Cloud Console

### 3. Rate Limiting
- Gemini API has daily quotas
- Monitor usage in [Google AI Studio](https://makersuite.google.com)

---

##  Production Checklist

Before deploying:

- [ ] API key added to environment variables
- [ ] `.env` file in `.gitignore`
- [ ] All dependencies in `requirements.txt`
- [ ] Test locally first (`streamlit run src/app.py`)
- [ ] Check for hardcoded paths (use relative paths)
- [ ] Verify all imports work
- [ ] Test export features (PDF/CSV generation)

---

##  Monitoring

### Streamlit Cloud:
- Built-in analytics dashboard
- View logs in real-time
- Monitor resource usage

### Heroku:
```bash
# View logs
heroku logs --tail

# Check app status
heroku ps
```

### Docker:
```bash
# View container logs
docker logs assetflow

# Monitor resources
docker stats assetflow
```

---

##  Updates & Maintenance

### Streamlit Cloud:
- Auto-deploys on Git push
- Redeploy manually: Settings → Reboot app

### Heroku:
```bash
git push heroku main
```

### Docker:
```bash
# Rebuild & restart
docker build -t assetflow .
docker stop assetflow
docker rm assetflow
docker run -p 8501:8501 assetflow
```

---

##  Troubleshooting

### "ModuleNotFoundError"
```bash
pip install -r requirements.txt
```

### "API Key Not Found"
- Check `.env` file exists in project root
- Verify `GEMINI_API_KEY=` is set correctly
- Restart app after adding key

### "PDF Generation Failed"
```bash
pip install reportlab
```

### Slow Scanning
- Use FAST mode (3 pages) for quick tests
- DEEP mode (15 pages) is slower but comprehensive

---

##  Support

Need help deploying?
-  Email: support@assetflow.com
-  GitHub Issues: [Report Issue](https://github.com/yourusername/AssetFlow/issues)

---

** Congratulations! AssetFlow is now live!**
