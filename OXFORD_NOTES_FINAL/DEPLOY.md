# Oxford LMS — Deployment Guide

## Why Netlify doesn't work

This is a **Flask/Python web application**.

Netlify is a **static site host**. It only serves pre-built HTML/CSS/JS files.
It cannot run Python, pip, gunicorn, or SQLAlchemy.

The "Page not found" error on Netlify is because the Python server is not running —
not a routing/redirect problem. A `_redirects` or `netlify.toml` file will NOT fix this.

---

## Correct deployment: Render.com

Render.com can run Python web services. The project is already configured for it.

### Steps

1. Go to https://render.com and sign in (GitHub login recommended)
2. Click **New → Web Service**
3. Connect your GitHub repository
4. Render will auto-detect `render.yaml` — click **Apply**
5. It will create:
   - A **Web Service** running gunicorn
   - A **PostgreSQL database** (free tier)
   - All environment variables (SECRET_KEY auto-generated, DATABASE_URL linked)
6. Wait for the build to finish (~3-5 minutes)
7. Your app is live at `https://oxford-lms.onrender.com` (or similar)

### Manual settings if not using render.yaml

| Setting | Value |
|---|---|
| Environment | Python 3 |
| Build Command | `pip install -r requirements-web.txt` |
| Start Command | `gunicorn web_app:app --workers 2 --bind 0.0.0.0:$PORT --timeout 120` |
| Environment Variables | `SECRET_KEY` (any random string), `DATABASE_URL` (from Render PostgreSQL) |

### Free tier note

Render's free tier spins down after 15 minutes of inactivity.
The first request after a spin-down takes ~30 seconds to load (cold start).
Upgrading to the $7/month plan removes this.

---

## Local development

```bash
cd OXFORD_NOTES_FINAL
python web_app.py
# Opens at http://127.0.0.1:5000
```

Default admin login: `admin` / `admin123`
