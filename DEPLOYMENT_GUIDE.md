# PromptForge Deployment Guide

## Overview

This guide walks you through deploying PromptForge to Heroku with automated CI/CD via GitHub Actions.

**What happens:**
1. You push code to GitHub → GitHub Actions runs tests
2. If tests pass ✅ → Automatic deployment to Heroku
3. Your app is live at `https://promptforge-yourname.herokuapp.com`

---

## Prerequisites

- ✅ GitHub account with this repo
- ✅ Heroku account (free tier available at https://www.heroku.com)
- ✅ Heroku CLI installed (Windows: https://devcenter.heroku.com/articles/heroku-cli)
- ✅ Ollama Cloud API key (already in your `.env`)

---

## Step 1: Create Heroku App

Open PowerShell and run:

```bash
# Login to Heroku
heroku login

# Create app with a unique name (replace "yourname" with something unique)
heroku create promptforge-yourname

# You'll see output like:
# Creating app... done, ⬢ promptforge-yourname
# https://promptforge-yourname.herokuapp.com/ | https://git.heroku.com/promptforge-yourname.git
```

**Save this app name** — you'll need it in the next steps.

---

## Step 2: Set Heroku Environment Variables

```bash
# Set your Ollama API key on Heroku
heroku config:set OLLAMA_API_KEY=your_api_key_here

# Verify it was set
heroku config

# Should show:
# === promptforge-yourname Config Vars
# OLLAMA_API_KEY: your_api_key_here
```

---

## Step 3: Get Heroku API Key

1. Go to https://dashboard.heroku.com/account/applications/authorizations
2. Scroll down to **Tokens**
3. Click **Create authorization**
4. Copy the token (this is your `HEROKU_API_KEY`)

---

## Step 4: Add GitHub Secrets

Go to your GitHub repo:

1. Click **Settings** tab
2. Left sidebar → **Secrets and variables** → **Actions**
3. Click **"New repository secret"** and add these 4 secrets:

| Secret Name | Value | Where to Find |
|-------------|-------|---------------|
| `HEROKU_API_KEY` | Your token from Step 3 | Heroku dashboard |
| `HEROKU_APP_NAME` | `promptforge-yourname` | From Step 1 output |
| `HEROKU_EMAIL` | Your Heroku email | Your Heroku account email |
| `OLLAMA_API_KEY` | Your API key | Your `.env` file |

**Important:** Do NOT include quotes. Just paste the value.

---

## Step 5: Push to GitHub

The GitHub Actions workflow files are already in your repo (`.github/workflows/ci-cd.yml`, `Procfile`, `runtime.txt`, `Dockerfile`).

Push them:

```bash
cd c:\Users\mustafa.waqar\Desktop\prompt-generator

# These files should already be staged, but make sure:
git add .github/ Procfile runtime.txt Dockerfile

# Commit
git commit -m "Add CI/CD and Heroku deployment configuration"

# Push to main (this triggers the workflow!)
git push origin main
```

---

## Step 6: Watch the Deployment

1. Go to your GitHub repo
2. Click **Actions** tab
3. You should see a workflow running: **"CI/CD Pipeline"**
4. Watch the steps:
   - 🧪 **test** job runs (pytest)
   - 🚀 **deploy** job runs (if test passes)

**What's happening in the test job:**
```
✅ Checkout code
✅ Set up Python 3.11
✅ Install dependencies (pip install -r requirements.txt)
✅ Run pytest tests/ -v
✅ Generate coverage report
```

**If tests pass:**
```
✅ Deploy to Heroku
✅ Build Python environment
✅ Install dependencies
✅ Start uvicorn server
✅ App is LIVE! 🎉
```

---

## Step 7: Access Your Live App

Once deployment completes, your app is live at:

```
https://promptforge-yourname.herokuapp.com
```

**Test it:**
- ✅ Open the URL in your browser
- ✅ Generate a prompt
- ✅ Copy button works
- ✅ History saves
- ✅ All features working

---

## Step 8: View Logs

If something goes wrong:

```bash
# See live logs
heroku logs --tail

# See last 50 lines
heroku logs --tail -n 50

# Follow logs in real-time
heroku logs --tail -f
```

---

## How CI/CD Works (Overview)

```
┌─────────────────────────────────────────┐
│ You push code to main branch on GitHub  │
└──────────────────┬──────────────────────┘
                   ↓
┌──────────────────────────────────────────┐
│ GitHub Actions Workflow Triggers        │
└──────────────────┬───────────────────────┘
                   ↓
        ┌──────────────────────┐
        │ RUN TESTS (pytest)   │
        └──────────┬───────────┘
                   ↓
         ┌─────────────────────┐
     ✅ │ All Tests Pass?      │ ❌
     ┌──┴──────────────────────┴───┐
     ↓                              ↓
┌─────────────┐         ┌──────────────────┐
│ DEPLOY TO   │         │ BUILD FAILED     │
│ HEROKU ✅   │         │ STOP HERE ❌     │
│ APP IS LIVE │         │ FIX & RETRY      │
└─────────────┘         └──────────────────┘
```

---

## Troubleshooting

### Tests keep failing
```bash
# Run tests locally to debug
pytest tests/ -v

# Fix issues, then push again
git add .
git commit -m "Fix tests"
git push origin main
```

### Deployment fails
```bash
# Check Heroku logs
heroku logs --tail -n 100

# Common issues:
# - Environment variable not set → heroku config:set KEY=value
# - Wrong Python version → Check runtime.txt
# - Missing dependency → Add to requirements.txt and push
```

### App crashes after deploy
```bash
# View real-time logs
heroku logs --tail -f

# Restart app
heroku restart

# Check config was set
heroku config
```

### "No such file or directory: Procfile"
Make sure `Procfile` exists in repo root:
```bash
git status

# Should show Procfile in the list. If not:
git add Procfile
git commit -m "Add Procfile"
git push origin main
```

---

## What Gets Deployed

The workflow deploys:
- ✅ All Python code (`src/`, `main.py`)
- ✅ Static files (`static/index.html`)
- ✅ Dependencies from `requirements.txt`
- ✅ Environment variables (via GitHub Secrets → Heroku Config)

**NOT deployed:**
- ❌ `.env` file (use GitHub Secrets instead)
- ❌ `venv/` directory (rebuilt automatically)
- ❌ `.git` folder (Git history)

---

## Making Changes After Deploy

To update your app after it's live:

```bash
# Make code changes locally
# ... edit files ...

# Test locally
pytest tests/ -v

# If tests pass, push to GitHub
git add .
git commit -m "Your commit message"
git push origin main

# GitHub Actions auto-deploys! 🎉
# Watch at: github.com/yourname/prompt-generator/actions
```

**No manual deployment needed!** Just push and it auto-deploys.

---

## Optional: Local Docker Testing

Test deployment locally before pushing:

```bash
# Build Docker image
docker build -t promptforge:latest .

# Run container
docker run -p 8000:8000 -e OLLAMA_API_KEY=your_key promptforge:latest

# Test at http://localhost:8000
# Ctrl+C to stop
```

---

## Workflow Status Badge

Add this to your `README.md` to show deployment status:

```markdown
[![CI/CD Pipeline](https://github.com/YOUR_USERNAME/prompt-generator/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/YOUR_USERNAME/prompt-generator/actions)
```

Replace `YOUR_USERNAME` with your GitHub username.

---

## Important Notes

⚠️ **Heroku Free Tier (as of April 2026):**
- May have limited free hours
- App sleeps after 30 minutes of inactivity
- Consider Railway.app or Render.com for unlimited free tier

✅ **Alternative Platforms** (same workflow, different config):
- Railway.app — Easy, good free tier
- Render.com — Modern, similar to Railway
- replit.com — Quick deployment, though slower

---

## Success Checklist

- [ ] Created Heroku app
- [ ] Set `OLLAMA_API_KEY` environment variable on Heroku
- [ ] Added 4 GitHub Secrets
- [ ] Pushed deployment files to main branch
- [ ] Watched CI/CD workflow complete successfully
- [ ] Accessed app at `https://promptforge-yourname.herokuapp.com`
- [ ] Tested generating a prompt
- [ ] Tested all core features

---

## Support

If you hit issues:

1. Check Heroku logs: `heroku logs --tail -n 100`
2. Check GitHub Actions: github.com/yourname/prompt-generator/actions
3. Verify environment variables: `heroku config`
4. Test locally first: `pytest tests/ -v`

---

**You're all set! Your PromptForge is now deployed with automatic CI/CD. 🚀**
