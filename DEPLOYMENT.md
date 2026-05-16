# Deployment Guide: Neon PostgreSQL + Streamlit Cloud

## Prerequisites
- GitHub account (to push your code)
- Neon account (neon.tech) - free tier available
- Streamlit Cloud account (share.streamlit.io)

## Step 1: Create Neon Database

1. Go to https://neon.tech and sign up
2. Create a new project
3. Go to "Connection string" and copy the full connection URL
   - Format: `postgresql://user:password@host/dbname`
4. Save it somewhere safe

## Step 2: Push to GitHub

```bash
cd "C:\Users\NotNe\OneDrive\Desktop\Big Data"
git add .
git commit -m "Add PostgreSQL setup for Streamlit Cloud deployment"
git push
```

## Step 3: Deploy to Streamlit Cloud

1. Go to https://share.streamlit.io
2. Sign in with GitHub
3. Click "New app"
4. Select your repository and `crypto-dashboard/app.py`
5. Click "Deploy"

## Step 4: Configure Secrets

In Streamlit Cloud, go to **Settings** → **Secrets** and add:

```
DATABASE_URL=postgresql://user:password@your-neon-host/your-db
COINGECKO_API_KEY=CG-zXo5Tmxb8jJni8rd7wZgf4ZR
```

## Step 5: Run Price Fetcher

The app is now live, but you need to keep the fetcher running:

### Option A: Local machine (simplest for now)
Keep running `python fetch_and_store.py` on your local machine 24/7

### Option B: Scheduled Cloud Function
- Use AWS Lambda + EventBridge
- Use Google Cloud Scheduler + Cloud Functions
- Use Railway/Heroku background job

## Notes

- The free Neon tier includes 3 GB storage (plenty for crypto prices)
- Free Streamlit Cloud resets daily but fetcher data persists in Neon
- Scale up when traffic increases ($5-20/month typical)
