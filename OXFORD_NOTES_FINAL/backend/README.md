# Oxford LMS - Backend

Python Flask backend with MongoDB database.

## Quick Start

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Configure Environment

Edit `.env` file and add your MongoDB connection string:

```env
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/oxford_lms?retryWrites=true&w=majority
DB_NAME=oxford_lms
SECRET_KEY=your-secret-key-here
```

### 3. Run the Application

```bash
python app.py
```

The server will start on `http://localhost:5000`

## Project Structure

```
backend/
├── app.py                 # Main Flask application
├── config.py              # Configuration settings
├── database_mongo.py      # MongoDB connection
├── models.py              # Legacy SQLAlchemy models (reference)
├── models_mongo.py        # MongoDB models
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (DO NOT COMMIT)
├── routes/                # API route blueprints
│   ├── auth.py           # Authentication endpoints
│   ├── students.py       # Student management
│   ├── courses.py        # Course management
│   ├── batches.py        # Batch management
│   ├── attendance.py     # Attendance tracking
│   ├── fees.py           # Fee management
│   ├── notes.py          # Notes/documents
│   ├── dashboard.py      # Dashboard data
│   ├── reports.py        # Reports generation
│   └── settings.py       # System settings
├── utils/                 # Utility functions
├── uploads/               # User uploaded files (NOT in Git)
├── exports/               # Generated exports (NOT in Git)
└── backups/               # Database backups (NOT in Git)
```

## API Endpoints

### Authentication
- `POST /api/auth/login` - User login
- `POST /api/auth/logout` - User logout
- `GET /api/auth/me` - Get current user
- `POST /api/auth/change-password` - Change password

### Students
- `GET /api/students/` - List students
- `POST /api/students/` - Create student
- `GET /api/students/<id>` - Get student details
- `PUT /api/students/<id>` - Update student
- `DELETE /api/students/<id>` - Delete student

### Courses
- `GET /api/courses/` - List courses
- `POST /api/courses/` - Create course
- `GET /api/courses/<id>` - Get course details
- `PUT /api/courses/<id>` - Update course
- `DELETE /api/courses/<id>` - Delete course

### Batches
- `GET /api/batches/` - List batches
- `POST /api/batches/` - Create batch
- `GET /api/batches/<id>` - Get batch details
- `PUT /api/batches/<id>` - Update batch
- `DELETE /api/batches/<id>` - Delete batch

### Attendance
- `GET /api/attendance/` - List attendance records
- `POST /api/attendance/` - Mark attendance
- `GET /api/attendance/student/<id>` - Get student attendance

### Fees
- `GET /api/fees/payments` - List fee payments
- `POST /api/fees/payments` - Record payment
- `GET /api/fees/receipts/<id>` - Get receipt

### Notes
- `GET /api/notes/` - List notes
- `POST /api/notes/` - Upload note
- `GET /api/notes/<id>` - Get note details
- `GET /api/notes/<id>/view` - View/stream file
- `GET /api/notes/<id>/download` - Download file

### Dashboard
- `GET /api/dashboard/stats` - Get dashboard statistics
- `GET /api/dashboard/recent-activities` - Recent activities

### Reports
- `GET /api/reports/students` - Student reports
- `GET /api/reports/attendance` - Attendance reports
- `GET /api/reports/fees` - Fee reports

## Default Login

- **Username:** admin
- **Password:** admin123

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `MONGODB_URI` | MongoDB connection string | Required |
| `DB_NAME` | Database name | oxford_lms |
| `SECRET_KEY` | Flask secret key | (change in production) |
| `MAX_UPLOAD_MB` | Max file upload size in MB | 500 |
| `FLASK_ENV` | Environment (development/production) | development |

## Development

```bash
# Run in debug mode
python app.py

# Or use Flask CLI
export FLASK_APP=app.py
flask run --debug
```

## Production Deployment

See `../DEPLOYMENT.md` for production deployment instructions.

## Security Notes

- Never commit `.env` file
- Change `SECRET_KEY` in production
- Use strong MongoDB credentials
- Whitelist IPs in MongoDB Atlas
- Enable HTTPS in production
