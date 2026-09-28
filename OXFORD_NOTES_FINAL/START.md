# Quick Start Guide

## ⚡ Get Oxford LMS Running in 3 Minutes

### Step 1: Configure MongoDB (2 minutes)

1. Edit `backend/.env` file
2. Replace the placeholder MongoDB URI with your actual connection string:

```env
MONGODB_URI=mongodb+srv://YOUR_USERNAME:YOUR_PASSWORD@YOUR_CLUSTER.mongodb.net/oxford_lms?retryWrites=true&w=majority
```

**Get your MongoDB URI:**
- Go to https://cloud.mongodb.com/
- Click "Connect" on your cluster
- Choose "Connect your application"
- Copy the connection string
- Replace `<username>` and `<password>` with your credentials

### Step 2: Install Dependencies (30 seconds)

```bash
cd backend
pip install -r requirements.txt
```

### Step 3: Run the Application (10 seconds)

```bash
python app.py
```

### Step 4: Open Browser

Go to: **http://localhost:5000**

**Login credentials:**
- Username: `admin`
- Password: `admin123`

---

## 🎉 That's it!

You should now see the Oxford LMS dashboard.

---

## 🆘 Having Issues?

### MongoDB Connection Failed
- Check your MongoDB URI in `backend/.env`
- Verify your IP is whitelisted in MongoDB Atlas (Network Access)
- Test your credentials

### Module Not Found
- Make sure you're in the `backend/` directory
- Run: `pip install -r requirements.txt`

### Templates Not Found
- Verify `frontend/templates/` directory exists
- Check that `frontend/static/` directory exists

### Port 5000 Already in Use
Edit `backend/app.py` and change the port:
```python
app.run(debug=True, host='0.0.0.0', port=5001)  # Changed to 5001
```

---

## 📚 Full Documentation

- **README.md** - Complete project overview
- **DEPLOYMENT.md** - Production deployment guide
- **backend/README.md** - Backend API documentation
- **frontend/README.md** - Frontend documentation
- **MONGODB_SETUP.md** - MongoDB configuration guide

---

## 🚀 Ready to Deploy?

See **DEPLOYMENT.md** for instructions on deploying to:
- Render.com (free tier available)
- Heroku
- Railway.app
- DigitalOcean
- Your own VPS

---

**Need help?** Check the troubleshooting sections in the documentation!
