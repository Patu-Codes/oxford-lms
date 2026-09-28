# Oxford LMS - MongoDB Setup Guide

## Quick Start

### 1. Get MongoDB Atlas Connection String

1. Visit [MongoDB Atlas](https://cloud.mongodb.com/)
2. Create a free cluster (if you haven't already)
3. Click "Connect" → "Connect your application"
4. Copy the connection string

### 2. Configure .env File

Edit `.env` and add your MongoDB connection string:

```env
MONGODB_URI=mongodb+srv://your_username:your_password@cluster.mongodb.net/oxford_lms?retryWrites=true&w=majority
DB_NAME=oxford_lms
SECRET_KEY=your-secret-key-change-this
```

### 3. Install Dependencies

```bash
pip install -r requirements-web.txt
```

### 4. Run Application

```bash
python web_app.py
```

## Default Login

- **Username:** admin
- **Password:** admin123

## Troubleshooting

### Connection Issues
- Whitelist your IP in MongoDB Atlas Network Access
- Verify username/password in connection string
- Check firewall settings

### Environment Variables Not Loading
- Ensure `.env` file is in the project root
- Check file encoding (should be UTF-8)
- Restart the application after changes

## MongoDB Collections

The application creates these collections automatically:
- users
- courses
- batches
- students
- student_fee_accounts
- fee_payments
- attendance
- notes
- favorites
- activity_logs
- notifications
- institute_settings

## Security

**Never commit `.env` file to version control!**

Add to `.gitignore`:
```
.env
__pycache__/
*.pyc
database/
venv/
```
