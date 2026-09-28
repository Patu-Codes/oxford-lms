# Oxford LMS - Learning Management System

Professional LMS for educational institutions with student management, attendance tracking, fee management, and notes distribution.

## 🏗️ Project Structure

```
oxford-lms/
├── frontend/              # HTML/CSS/JavaScript frontend
│   ├── static/           # CSS, JS, images
│   ├── templates/        # HTML templates
│   └── assets/           # Logo and assets
│
├── backend/               # Python Flask backend
│   ├── app.py            # Main application
│   ├── config.py         # Configuration
│   ├── models_mongo.py   # MongoDB models
│   ├── database_mongo.py # Database connection
│   ├── routes/           # API endpoints
│   ├── utils/            # Helper functions
│   ├── uploads/          # User uploads
│   ├── exports/          # Generated files
│   └── backups/          # Database backups
│
├── .env                   # Environment variables (not in Git)
├── .env.example          # Environment template
└── README.md             # This file
```

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- MongoDB Atlas account (free tier available)
- pip package manager

### Installation

1. **Clone the repository**
   ```bash
   cd oxford-lms
   ```

2. **Set up backend**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

3. **Configure environment**
   ```bash
   # Copy .env.example to .env
   cp .env.example .env
   
   # Edit .env and add your MongoDB connection string
   # Get it from https://cloud.mongodb.com/
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Open browser**
   ```
   http://localhost:5000
   ```

### Default Login
- **Username:** admin
- **Password:** admin123

## 📚 Features

### Student Management
- Complete student profiles
- Course enrollment
- Batch assignment
- Guardian information
- Profile photos
- Status tracking (active/inactive/completed)

### Attendance System
- Daily attendance marking
- Batch-wise tracking
- Attendance reports
- Percentage calculation
- History view

### Fee Management
- Fee structure per student
- Payment recording
- Receipt generation (PDF)
- Payment history
- Multiple payment modes (Cash, UPI, Bank Transfer, Cheque)
- Institute settings for receipts

### Notes Distribution
- PDF, DOC, PPT, video upload
- View-only or downloadable mode
- Course/Batch filtering
- Category organization
- Search and tags
- View/download tracking
- Watermarking for protected content

### Course & Batch Management
- Course catalog
- Batch scheduling
- Faculty assignment
- Enrollment limits
- Status management

### Reports & Analytics
- Student reports
- Attendance reports
- Fee collection reports
- Export to PDF/Excel

### User Roles
- **Admin:** Full system access
- **Faculty:** Teaching and attendance
- **Student:** View notes, attendance, fees

## 🛠️ Technology Stack

### Backend
- **Framework:** Flask 3.0
- **Database:** MongoDB (via pymongo)
- **Authentication:** Session-based
- **File Storage:** Local filesystem
- **PDF Generation:** ReportLab
- **Image Processing:** Pillow

### Frontend
- **HTML5/CSS3:** Modern responsive design
- **JavaScript:** Vanilla JS (no framework)
- **Icons:** Inline SVG
- **PDF Viewer:** PDF.js
- **Video Player:** HTML5 video

## 📖 Documentation

- [Backend Documentation](backend/README.md)
- [Frontend Documentation](frontend/README.md)
- [MongoDB Setup Guide](backend/MONGODB_SETUP.md)
- [Deployment Guide](DEPLOYMENT.md)

## 🔧 Configuration

### Environment Variables

Create `backend/.env` file:

```env
# MongoDB Connection
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/oxford_lms?retryWrites=true&w=majority
DB_NAME=oxford_lms

# Application
SECRET_KEY=your-secret-key-here-change-in-production
FLASK_ENV=development

# File Upload
MAX_UPLOAD_MB=500
```

### MongoDB Atlas Setup

1. Create account at [MongoDB Atlas](https://cloud.mongodb.com/)
2. Create a free cluster
3. Add database user
4. Whitelist IP addresses
5. Get connection string
6. Add to `.env` file

## 🚢 Deployment

### Development
```bash
cd backend
python app.py
```

### Production (Render/Heroku/Railway)
```bash
# Uses Procfile and wsgi.py
gunicorn wsgi:app
```

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed deployment instructions.

## 🔒 Security

- MongoDB connection with authentication
- Session-based authentication
- Role-based access control
- File upload validation
- SQL injection prevention (NoSQL)
- XSS protection
- CSRF protection
- Secure password hashing (SHA-256)

## 📱 Responsive Design

- Mobile-friendly interface
- Collapsible sidebar
- Touch-optimized controls
- Responsive tables
- Adaptive layouts

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## 📄 License

This project is proprietary software for Oxford LMS.

## 👥 Support

For support and queries:
- Email: admin@oxford.edu
- Documentation: See `/docs` folder

## 🎓 Credits

Developed for Oxford Learning Management System
Version 4.0 - MongoDB Edition

---

**Note:** This project has been reorganized with separate frontend/ and backend/ directories for clean deployment and maintenance.
