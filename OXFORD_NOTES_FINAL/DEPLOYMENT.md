# Oxford LMS - Deployment Guide

Complete guide for deploying Oxford LMS to production.

## 📋 Pre-Deployment Checklist

- [ ] MongoDB Atlas cluster created
- [ ] Database user with appropriate permissions
- [ ] IP whitelist configured
- [ ] `.env` file configured with production values
- [ ] Changed default admin password
- [ ] SECRET_KEY set to secure random value
- [ ] Tested application locally

## 🚀 Deployment Options

### Option 1: Render.com (Recommended - Free Tier Available)

1. **Create Render Account**
   - Go to [render.com](https://render.com/)
   - Sign up with GitHub

2. **Create Web Service**
   - Click "New +" → "Web Service"
   - Connect your repository
   - Configure:
     - **Name:** oxford-lms
     - **Root Directory:** backend
     - **Environment:** Python 3
     - **Build Command:** `pip install -r requirements.txt`
     - **Start Command:** `gunicorn wsgi:app`

3. **Add Environment Variables**
   ```
   MONGODB_URI=mongodb+srv://...
   DB_NAME=oxford_lms
   SECRET_KEY=<generate-random-key>
   FLASK_ENV=production
   MAX_UPLOAD_MB=500
   ```

4. **Deploy**
   - Click "Create Web Service"
   - Wait for deployment
   - Access at `https://oxford-lms.onrender.com`

### Option 2: Heroku

1. **Install Heroku CLI**
   ```bash
   # Download from https://devcenter.heroku.com/articles/heroku-cli
   ```

2. **Login and Create App**
   ```bash
   heroku login
   cd backend
   heroku create oxford-lms
   ```

3. **Set Environment Variables**
   ```bash
   heroku config:set MONGODB_URI="mongodb+srv://..."
   heroku config:set DB_NAME="oxford_lms"
   heroku config:set SECRET_KEY="<random-key>"
   heroku config:set FLASK_ENV="production"
   ```

4. **Deploy**
   ```bash
   git push heroku main
   heroku open
   ```

### Option 3: Railway.app

1. **Create Railway Account**
   - Go to [railway.app](https://railway.app/)
   - Connect GitHub

2. **Deploy from GitHub**
   - New Project → Deploy from GitHub
   - Select repository
   - Set root directory to `backend`

3. **Add Environment Variables**
   - Go to Variables tab
   - Add all required environment variables

4. **Configure Start Command**
   - Settings → Start Command: `gunicorn wsgi:app`

### Option 4: DigitalOcean App Platform

1. **Create DigitalOcean Account**
   - Go to [digitalocean.com](https://www.digitalocean.com/)

2. **Create App**
   - Apps → Create App
   - Connect GitHub repository
   - Configure:
     - **Type:** Web Service
     - **Source Directory:** backend
     - **Run Command:** `gunicorn wsgi:app`

3. **Add Environment Variables**
   - Add all required variables in App settings

### Option 5: VPS (Ubuntu/Debian)

1. **SSH into Server**
   ```bash
   ssh user@your-server-ip
   ```

2. **Install Dependencies**
   ```bash
   sudo apt update
   sudo apt install python3 python3-pip python3-venv nginx
   ```

3. **Clone Repository**
   ```bash
   cd /var/www
   git clone <your-repo-url> oxford-lms
   cd oxford-lms/backend
   ```

4. **Create Virtual Environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   pip install gunicorn
   ```

5. **Configure Environment**
   ```bash
   nano .env
   # Add your environment variables
   ```

6. **Create Systemd Service**
   ```bash
   sudo nano /etc/systemd/system/oxford-lms.service
   ```

   ```ini
   [Unit]
   Description=Oxford LMS
   After=network.target

   [Service]
   User=www-data
   WorkingDirectory=/var/www/oxford-lms/backend
   Environment="PATH=/var/www/oxford-lms/backend/venv/bin"
   ExecStart=/var/www/oxford-lms/backend/venv/bin/gunicorn --workers 3 --bind 127.0.0.1:5000 wsgi:app

   [Install]
   WantedBy=multi-user.target
   ```

7. **Start Service**
   ```bash
   sudo systemctl start oxford-lms
   sudo systemctl enable oxford-lms
   ```

8. **Configure Nginx**
   ```bash
   sudo nano /etc/nginx/sites-available/oxford-lms
   ```

   ```nginx
   server {
       listen 80;
       server_name your-domain.com;

       location / {
           proxy_pass http://127.0.0.1:5000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }

       location /static {
           alias /var/www/oxford-lms/frontend/static;
       }

       client_max_body_size 500M;
   }
   ```

9. **Enable Site**
   ```bash
   sudo ln -s /etc/nginx/sites-available/oxford-lms /etc/nginx/sites-enabled/
   sudo nginx -t
   sudo systemctl restart nginx
   ```

10. **SSL with Let's Encrypt**
    ```bash
    sudo apt install certbot python3-certbot-nginx
    sudo certbot --nginx -d your-domain.com
    ```

## 🔐 Production Security

### 1. Generate Secure SECRET_KEY

```python
import secrets
print(secrets.token_hex(32))
```

Add to environment variables.

### 2. MongoDB Atlas Security

- Enable IP Whitelist (add deployment server IP)
- Use strong database password
- Enable database encryption
- Set up database backups
- Monitor access logs

### 3. Change Default Credentials

```python
# After first deployment, login and change admin password
# Go to Profile → Change Password
```

### 4. File Upload Security

- Limit file sizes (MAX_UPLOAD_MB in .env)
- Validate file types
- Scan uploads (optional: integrate antivirus)

### 5. Enable HTTPS

- Use Let's Encrypt (free SSL)
- Force HTTPS redirects
- Set secure session cookies

## 📊 Monitoring

### Application Logs

**Render/Heroku/Railway:**
- Check platform dashboard for logs

**VPS:**
```bash
sudo journalctl -u oxford-lms -f
```

### MongoDB Monitoring

- Use MongoDB Atlas monitoring dashboard
- Set up alerts for performance issues
- Monitor connection pool usage

### Health Check

Access `/health` endpoint:
```bash
curl https://your-domain.com/health
```

Expected response:
```json
{
  "status": "healthy",
  "app": "Oxford LMS",
  "version": "4.0",
  "database": "MongoDB"
}
```

## 🔄 Updates and Maintenance

### Updating Application

**Git-based platforms (Render/Heroku/Railway):**
```bash
git push origin main
# Automatic deployment
```

**VPS:**
```bash
cd /var/www/oxford-lms
git pull origin main
cd backend
source venv/bin/activate
pip install -r requirements.txt
sudo systemctl restart oxford-lms
```

### Database Backup

**Manual Backup:**
```bash
mongodump --uri="mongodb+srv://..." --out=backup/
```

**Automated Backup:**
- Use MongoDB Atlas automated backups (paid tier)
- Schedule cron job for mongodump

### File Backup

```bash
# Backup uploads, exports, backups directories
tar -czf oxford-lms-files-$(date +%Y%m%d).tar.gz backend/uploads backend/exports backend/backups
```

## 🐛 Troubleshooting

### Application Won't Start

1. Check environment variables
2. Verify MongoDB connection string
3. Check logs for Python errors
4. Ensure all dependencies installed

### Database Connection Failed

1. Verify MONGODB_URI is correct
2. Check IP whitelist in MongoDB Atlas
3. Test connection with mongo shell
4. Check network connectivity

### File Upload Issues

1. Check MAX_UPLOAD_MB setting
2. Verify disk space
3. Check directory permissions
4. Review nginx/platform upload limits

### Static Files Not Loading

1. Verify frontend path in app.py
2. Check static folder exists
3. Clear browser cache
4. Check nginx static file configuration

## 📱 Mobile App Integration (Future)

If building mobile apps:
- API is at `/api/*` endpoints
- Use JWT tokens for mobile auth
- Enable CORS for mobile domains

## 🎯 Performance Optimization

### 1. Database Indexing
MongoDB indexes are created automatically on first run.

### 2. Caching
Consider adding Redis for session storage and caching.

### 3. CDN
Use CDN for static assets (CSS, JS, images).

### 4. Compression
Enable gzip compression in nginx.

### 5. Connection Pool
MongoDB connection pool is managed automatically.

## 📞 Support

For deployment support:
- Check documentation
- Review logs
- Contact system administrator

---

**Important:** Always test thoroughly in staging environment before production deployment!
