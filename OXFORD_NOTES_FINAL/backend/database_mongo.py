"""
MongoDB Database Configuration and Connection for Oxford LMS
"""
import os
from pymongo import MongoClient, ASCENDING, DESCENDING
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# MongoDB Connection
MONGODB_URI = os.environ.get('MONGODB_URI')
DB_NAME = os.environ.get('DB_NAME', 'oxford_lms')

# Global MongoDB client and database
_client = None
_db = None


def get_db():
    """Get MongoDB database instance (lazy initialization)"""
    global _client, _db
    
    if _db is None:
        if not MONGODB_URI:
            raise ValueError("MONGODB_URI not set in environment variables. Please configure .env file.")
        
        try:
            _client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=5000)
            # Test connection
            _client.admin.command('ping')
            _db = _client[DB_NAME]
            print(f"✓ Connected to MongoDB: {DB_NAME}")
        except (ConnectionFailure, ServerSelectionTimeoutError) as e:
            print(f"✗ MongoDB connection failed: {e}")
            raise
    
    return _db


def close_db():
    """Close MongoDB connection"""
    global _client, _db
    if _client:
        _client.close()
        _client = None
        _db = None
        print("✓ MongoDB connection closed")


def init_db():
    """Initialize MongoDB collections and indexes"""
    db = get_db()
    
    # Create collections (MongoDB creates them automatically on first insert)
    collections = [
        'users', 'courses', 'batches', 'students', 'student_fee_accounts',
        'fee_payments', 'fee_accounts', 'attendance', 'notes', 'favorites',
        'activity_logs', 'notifications', 'institute_settings',
        'assignments', 'certificates'
    ]
    
    for collection in collections:
        if collection not in db.list_collection_names():
            db.create_collection(collection)
    
    # Create indexes for better query performance
    print("Creating indexes...")
    
    # Users
    db.users.create_index([('username', ASCENDING)], unique=True)
    db.users.create_index([('email', ASCENDING)])
    db.users.create_index([('role', ASCENDING)])
    
    # Courses
    db.courses.create_index([('name', ASCENDING)], unique=True)
    db.courses.create_index([('code', ASCENDING)], unique=True, sparse=True)
    db.courses.create_index([('status', ASCENDING)])
    
    # Batches
    db.batches.create_index([('code', ASCENDING)], unique=True, sparse=True)
    db.batches.create_index([('course_id', ASCENDING)])
    db.batches.create_index([('status', ASCENDING)])
    
    # Students
    db.students.create_index([('student_id', ASCENDING)], unique=True)
    db.students.create_index([('user_id', ASCENDING)], unique=True, sparse=True)
    db.students.create_index([('course_id', ASCENDING)])
    db.students.create_index([('batch_id', ASCENDING)])
    db.students.create_index([('status', ASCENDING)])
    
    # Student Fee Accounts
    db.student_fee_accounts.create_index([('student_id', ASCENDING)], unique=True)
    
    # Fee Payments
    db.fee_payments.create_index([('student_id', ASCENDING)])
    db.fee_payments.create_index([('payment_date', DESCENDING)])
    db.fee_payments.create_index([('receipt_number', ASCENDING)], unique=True, sparse=True)
    
    # Attendance
    db.attendance.create_index([('student_id', ASCENDING), ('date', ASCENDING)], unique=True)
    db.attendance.create_index([('batch_id', ASCENDING)])
    db.attendance.create_index([('date', DESCENDING)])
    
    # Notes
    db.notes.create_index([('uploaded_by', ASCENDING)])
    db.notes.create_index([('course_id', ASCENDING)])
    db.notes.create_index([('batch_id', ASCENDING)])
    db.notes.create_index([('uploaded_at', DESCENDING)])
    db.notes.create_index([('category', ASCENDING)])
    
    # Favorites
    db.favorites.create_index([('user_id', ASCENDING), ('note_id', ASCENDING)], unique=True)
    
    # Activity Logs
    db.activity_logs.create_index([('user_id', ASCENDING)])
    db.activity_logs.create_index([('timestamp', DESCENDING)])
    
    # Notifications
    db.notifications.create_index([('user_id', ASCENDING)])
    db.notifications.create_index([('created_at', DESCENDING)])
    db.notifications.create_index([('is_read', ASCENDING)])
    
    print("✓ Indexes created successfully")
    
    # Create default admin user if not exists
    create_default_data()


def create_default_data():
    """Create default admin user and courses"""
    db = get_db()
    
    # Check if admin exists
    if not db.users.find_one({'username': 'admin'}):
        import hashlib
        admin = {
            'username': 'admin',
            'password': hashlib.sha256('admin123'.encode()).hexdigest(),
            'role': 'admin',
            'email': 'admin@oxford.edu',
            'full_name': 'System Administrator',
            'profile_image': None,
            'created_at': datetime.utcnow(),
            'last_login': None,
            'is_active': True
        }
        db.users.insert_one(admin)
        print("✓ Default admin user created (username: admin, password: admin123)")
    
    # Default courses
    default_courses = [
        {'name': 'Python Programming', 'code': 'PY', 'duration': '6 Months', 'default_fee': 30000},
        {'name': 'Data Science', 'code': 'DS', 'duration': '9 Months', 'default_fee': 50000},
        {'name': 'Web Development', 'code': 'WD', 'duration': '6 Months', 'default_fee': 35000},
        {'name': 'Machine Learning', 'code': 'ML', 'duration': '12 Months', 'default_fee': 70000},
        {'name': 'Cloud Computing', 'code': 'CC', 'duration': '12 Months', 'default_fee': 70000},
    ]
    
    for course_data in default_courses:
        if not db.courses.find_one({'name': course_data['name']}):
            course_data.update({
                'description': None,
                'status': 'active',
                'created_at': datetime.utcnow()
            })
            db.courses.insert_one(course_data)
    
    print("✓ Default courses created")
    
    # Default institute settings
    if not db.institute_settings.find_one():
        settings = {
            'institute_name': 'Oxford LMS',
            'institute_address': '',
            'institute_phone': '',
            'institute_email': '',
            'institute_website': '',
            'receipt_prefix': 'OXLMS',
            'receipt_footer': 'Thank you for your payment.',
            'authorized_signatory': 'Administrator',
            'currency_symbol': 'Rs.',
            'updated_at': datetime.utcnow()
        }
        db.institute_settings.insert_one(settings)
        print("✓ Default institute settings created")
    
    print("✓ Oxford LMS MongoDB database initialized")


# Helper functions for ObjectId conversion
from bson import ObjectId

def to_object_id(id_value):
    """Convert string ID to ObjectId if valid"""
    if id_value is None:
        return None
    if isinstance(id_value, ObjectId):
        return id_value
    try:
        return ObjectId(id_value)
    except:
        return None


def serialize_doc(doc):
    """Convert MongoDB document to JSON-serializable dict"""
    if doc is None:
        return None
    
    if isinstance(doc, list):
        return [serialize_doc(d) for d in doc]
    
    # Convert ObjectId to string
    if '_id' in doc:
        doc['id'] = str(doc['_id'])
        del doc['_id']
    
    # Convert datetime to ISO format
    for key, value in doc.items():
        if isinstance(value, datetime):
            doc[key] = value.isoformat()
        elif isinstance(value, ObjectId):
            doc[key] = str(value)
    
    return doc


# Password hashing utilities
import hashlib

def hash_password(password):
    """Hash password using SHA256"""
    return hashlib.sha256(password.encode()).hexdigest()


def check_password(password, hashed):
    """Verify password against hash"""
    return hash_password(password) == hashed
