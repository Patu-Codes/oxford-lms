"""
MongoDB Models for Oxford LMS
Provides similar interface to Flask-SQLAlchemy models for easier migration
"""
from datetime import datetime
from database_mongo import get_db, to_object_id, serialize_doc, hash_password, check_password
from bson import ObjectId


class MongoModel:
    """Base class for MongoDB models"""
    collection_name = None
    
    @classmethod
    def get_collection(cls):
        """Get MongoDB collection for this model"""
        db = get_db()
        return db[cls.collection_name]
    
    @classmethod
    def find_one(cls, filter_dict):
        """Find one document"""
        doc = cls.get_collection().find_one(filter_dict)
        return serialize_doc(doc) if doc else None
    
    @classmethod
    def find_by_id(cls, doc_id):
        """Find document by ID"""
        obj_id = to_object_id(doc_id)
        if not obj_id:
            return None
        return cls.find_one({'_id': obj_id})
    
    @classmethod
    def find(cls, filter_dict=None, sort=None, skip=0, limit=0):
        """Find multiple documents"""
        filter_dict = filter_dict or {}
        cursor = cls.get_collection().find(filter_dict)
        if sort:
            cursor = cursor.sort(sort)
        if skip:
            cursor = cursor.skip(skip)
        if limit:
            cursor = cursor.limit(limit)
        return [serialize_doc(doc) for doc in cursor]
    
    @classmethod
    def count(cls, filter_dict=None):
        """Count documents"""
        filter_dict = filter_dict or {}
        return cls.get_collection().count_documents(filter_dict)
    
    @classmethod
    def insert_one(cls, document):
        """Insert a document"""
        result = cls.get_collection().insert_one(document)
        return str(result.inserted_id)
    
    @classmethod
    def update_one(cls, filter_dict, update_dict):
        """Update a document"""
        result = cls.get_collection().update_one(filter_dict, {'$set': update_dict})
        return result.modified_count
    
    @classmethod
    def delete_one(cls, filter_dict):
        """Delete a document"""
        result = cls.get_collection().delete_one(filter_dict)
        return result.deleted_count
    
    @classmethod
    def update_by_id(cls, doc_id, update_dict):
        """Update document by ID"""
        obj_id = to_object_id(doc_id)
        if not obj_id:
            return 0
        return cls.update_one({'_id': obj_id}, update_dict)
    
    @classmethod
    def delete_by_id(cls, doc_id):
        """Delete document by ID"""
        obj_id = to_object_id(doc_id)
        if not obj_id:
            return 0
        return cls.delete_one({'_id': obj_id})


# ─── USER ─────────────────────────────────────────────────────────────────────

class User(MongoModel):
    collection_name = 'users'
    
    @classmethod
    def create(cls, username, password, role, email=None, full_name=None, profile_image=None):
        """Create new user"""
        user = {
            'username': username,
            'password': hash_password(password),
            'role': role,
            'email': email,
            'full_name': full_name,
            'profile_image': profile_image,
            'created_at': datetime.utcnow(),
            'last_login': None,
            'is_active': True
        }
        return cls.insert_one(user)
    
    @classmethod
    def find_by_username(cls, username):
        """Find user by username"""
        return cls.find_one({'username': username})
    
    @classmethod
    def verify_password(cls, user, password):
        """Verify user password"""
        if not user:
            return False
        return check_password(password, user.get('password', ''))
    
    @classmethod
    def update_password(cls, user_id, new_password):
        """Update user password"""
        return cls.update_by_id(user_id, {'password': hash_password(new_password)})
    
    @classmethod
    def update_last_login(cls, user_id):
        """Update last login timestamp"""
        return cls.update_by_id(user_id, {'last_login': datetime.utcnow()})


# ─── COURSE ───────────────────────────────────────────────────────────────────

class Course(MongoModel):
    collection_name = 'courses'
    
    @classmethod
    def create(cls, name, code=None, description=None, duration=None, default_fee=0, status='active'):
        """Create new course"""
        course = {
            'name': name,
            'code': code,
            'description': description,
            'duration': duration,
            'default_fee': default_fee,
            'status': status,
            'created_at': datetime.utcnow()
        }
        return cls.insert_one(course)
    
    @classmethod
    def find_by_name(cls, name):
        """Find course by name"""
        return cls.find_one({'name': name})
    
    @classmethod
    def find_active(cls):
        """Find all active courses"""
        return cls.find({'status': 'active'}, sort=[('name', 1)])


# ─── BATCH ────────────────────────────────────────────────────────────────────

class Batch(MongoModel):
    collection_name = 'batches'
    
    @classmethod
    def create(cls, name, code=None, course_id=None, **kwargs):
        """Create new batch"""
        batch = {
            'name': name,
            'code': code,
            'course_id': course_id,
            'faculty': kwargs.get('faculty'),
            'start_date': kwargs.get('start_date'),
            'end_date': kwargs.get('end_date'),
            'start_time': kwargs.get('start_time'),
            'end_time': kwargs.get('end_time'),
            'schedule': kwargs.get('schedule'),
            'max_students': kwargs.get('max_students'),
            'status': kwargs.get('status', 'active'),
            'created_at': datetime.utcnow()
        }
        return cls.insert_one(batch)
    
    @classmethod
    def find_by_course(cls, course_id):
        """Find batches by course ID"""
        return cls.find({'course_id': course_id}, sort=[('name', 1)])
    
    @classmethod
    def find_active(cls):
        """Find all active batches"""
        return cls.find({'status': 'active'}, sort=[('name', 1)])


# ─── STUDENT ──────────────────────────────────────────────────────────────────

class Student(MongoModel):
    collection_name = 'students'
    
    @classmethod
    def create(cls, student_id, first_name, last_name, **kwargs):
        """Create new student"""
        student = {
            'user_id': kwargs.get('user_id'),
            'student_id': student_id,
            'first_name': first_name,
            'last_name': last_name,
            'date_of_birth': kwargs.get('date_of_birth'),
            'gender': kwargs.get('gender'),
            'email': kwargs.get('email'),
            'phone': kwargs.get('phone'),
            'address': kwargs.get('address'),
            'course_id': kwargs.get('course_id'),
            'course': kwargs.get('course'),
            'batch_id': kwargs.get('batch_id'),
            'batch': kwargs.get('batch'),
            'enrollment_date': kwargs.get('enrollment_date'),
            'joining_date': kwargs.get('joining_date'),
            'profile_image': kwargs.get('profile_image'),
            'guardian_name': kwargs.get('guardian_name'),
            'guardian_phone': kwargs.get('guardian_phone'),
            'status': kwargs.get('status', 'active'),
            'is_active': kwargs.get('is_active', True),
            'total_fee': kwargs.get('total_fee'),
            'fee_remarks': kwargs.get('fee_remarks')
        }
        return cls.insert_one(student)
    
    @classmethod
    def find_by_student_id(cls, student_id):
        """Find student by student ID"""
        return cls.find_one({'student_id': student_id})
    
    @classmethod
    def find_by_user_id(cls, user_id):
        """Find student by user ID"""
        return cls.find_one({'user_id': user_id})
    
    @classmethod
    def find_by_course(cls, course_id):
        """Find students by course ID"""
        return cls.find({'course_id': course_id}, sort=[('first_name', 1)])
    
    @classmethod
    def find_by_batch(cls, batch_id):
        """Find students by batch ID"""
        return cls.find({'batch_id': batch_id}, sort=[('first_name', 1)])
    
    @classmethod
    def search(cls, query, course_id=None, batch_id=None, status=None, active_only=True, skip=0, limit=50):
        """Search students with filters"""
        filter_dict = {}
        
        if query:
            filter_dict['$or'] = [
                {'first_name': {'$regex': query, '$options': 'i'}},
                {'last_name': {'$regex': query, '$options': 'i'}},
                {'student_id': {'$regex': query, '$options': 'i'}},
                {'email': {'$regex': query, '$options': 'i'}}
            ]
        
        if course_id:
            filter_dict['course_id'] = course_id
        if batch_id:
            filter_dict['batch_id'] = batch_id
        if status:
            filter_dict['status'] = status
        if active_only:
            filter_dict['is_active'] = True
        
        total = cls.count(filter_dict)
        students = cls.find(filter_dict, sort=[('first_name', 1)], skip=skip, limit=limit)
        
        return {
            'students': students,
            'total': total,
            'pages': (total + limit - 1) // limit if limit > 0 else 1,
            'current_page': (skip // limit) + 1 if limit > 0 else 1
        }


# ─── STUDENT FEE ACCOUNT ──────────────────────────────────────────────────────

class StudentFeeAccount(MongoModel):
    collection_name = 'student_fee_accounts'
    
    @classmethod
    def create(cls, student_id, total_fee, **kwargs):
        """Create fee account for student"""
        account = {
            'student_id': student_id,
            'total_fee': total_fee,
            'installment_amount': kwargs.get('installment_amount'),
            'installment_freq': kwargs.get('installment_freq'),
            'next_due_date': kwargs.get('next_due_date'),
            'remarks': kwargs.get('remarks'),
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }
        return cls.insert_one(account)
    
    @classmethod
    def find_by_student(cls, student_id):
        """Find fee account by student ID"""
        return cls.find_one({'student_id': student_id})


# ─── FEE PAYMENT ──────────────────────────────────────────────────────────────

class FeePayment(MongoModel):
    collection_name = 'fee_payments'
    
    @classmethod
    def create(cls, student_id, amount, payment_date, **kwargs):
        """Create fee payment record"""
        payment = {
            'student_id': student_id,
            'course_id': kwargs.get('course_id'),
            'batch_id': kwargs.get('batch_id'),
            'amount': amount,
            'payment_date': payment_date,
            'payment_mode': kwargs.get('payment_mode'),
            'transaction_id': kwargs.get('transaction_id'),
            'receipt_number': kwargs.get('receipt_number'),
            'remarks': kwargs.get('remarks'),
            'collected_by': kwargs.get('collected_by'),
            'institute_name': kwargs.get('institute_name'),
            'created_at': datetime.utcnow()
        }
        return cls.insert_one(payment)
    
    @classmethod
    def find_by_student(cls, student_id):
        """Find payments by student ID"""
        return cls.find({'student_id': student_id}, sort=[('payment_date', -1)])
    
    @classmethod
    def find_by_receipt_number(cls, receipt_number):
        """Find payment by receipt number"""
        return cls.find_one({'receipt_number': receipt_number})


# ─── ATTENDANCE ───────────────────────────────────────────────────────────────

class Attendance(MongoModel):
    collection_name = 'attendance'
    
    @classmethod
    def create(cls, student_id, date, status, **kwargs):
        """Create attendance record"""
        attendance = {
            'student_id': student_id,
            'batch_id': kwargs.get('batch_id'),
            'date': date,
            'status': status,
            'remarks': kwargs.get('remarks'),
            'marked_by': kwargs.get('marked_by'),
            'marked_at': datetime.utcnow()
        }
        return cls.insert_one(attendance)
    
    @classmethod
    def find_by_student(cls, student_id, start_date=None, end_date=None):
        """Find attendance records for student"""
        filter_dict = {'student_id': student_id}
        if start_date or end_date:
            filter_dict['date'] = {}
            if start_date:
                filter_dict['date']['$gte'] = start_date
            if end_date:
                filter_dict['date']['$lte'] = end_date
        return cls.find(filter_dict, sort=[('date', -1)])
    
    @classmethod
    def find_by_date(cls, date, batch_id=None):
        """Find attendance records for a date"""
        filter_dict = {'date': date}
        if batch_id:
            filter_dict['batch_id'] = batch_id
        return cls.find(filter_dict)


# ─── NOTE ─────────────────────────────────────────────────────────────────────

class Note(MongoModel):
    collection_name = 'notes'
    
    @classmethod
    def create(cls, title, file_path, **kwargs):
        """Create note/document"""
        note = {
            'title': title,
            'description': kwargs.get('description'),
            'category': kwargs.get('category'),
            'course_id': kwargs.get('course_id'),
            'batch_id': kwargs.get('batch_id'),
            'file_path': file_path,
            'file_type': kwargs.get('file_type'),
            'file_size': kwargs.get('file_size'),
            'uploaded_by': kwargs.get('uploaded_by'),
            'uploaded_at': datetime.utcnow(),
            'visibility': kwargs.get('visibility', 'all'),
            'views': 0,
            'downloads': 0,
            'tags': kwargs.get('tags'),
            'is_downloadable': kwargs.get('is_downloadable', False)
        }
        return cls.insert_one(note)
    
    @classmethod
    def increment_views(cls, note_id):
        """Increment view count"""
        obj_id = to_object_id(note_id)
        if obj_id:
            cls.get_collection().update_one({'_id': obj_id}, {'$inc': {'views': 1}})
    
    @classmethod
    def increment_downloads(cls, note_id):
        """Increment download count"""
        obj_id = to_object_id(note_id)
        if obj_id:
            cls.get_collection().update_one({'_id': obj_id}, {'$inc': {'downloads': 1}})


# ─── FAVORITE ─────────────────────────────────────────────────────────────────

class Favorite(MongoModel):
    collection_name = 'favorites'
    
    @classmethod
    def create(cls, user_id, note_id):
        """Create favorite"""
        favorite = {
            'user_id': user_id,
            'note_id': note_id,
            'created_at': datetime.utcnow()
        }
        return cls.insert_one(favorite)
    
    @classmethod
    def find_by_user(cls, user_id):
        """Find user's favorites"""
        return cls.find({'user_id': user_id}, sort=[('created_at', -1)])
    
    @classmethod
    def remove(cls, user_id, note_id):
        """Remove favorite"""
        return cls.delete_one({'user_id': user_id, 'note_id': note_id})


# ─── ACTIVITY LOG ─────────────────────────────────────────────────────────────

class ActivityLog(MongoModel):
    collection_name = 'activity_logs'
    
    @classmethod
    def create(cls, action, **kwargs):
        """Create activity log"""
        log = {
            'user_id': kwargs.get('user_id'),
            'action': action,
            'details': kwargs.get('details'),
            'status': kwargs.get('status', 'SUCCESS'),
            'ip_address': kwargs.get('ip_address'),
            'timestamp': datetime.utcnow()
        }
        return cls.insert_one(log)
    
    @classmethod
    def find_by_user(cls, user_id, limit=100):
        """Find user's activity logs"""
        return cls.find({'user_id': user_id}, sort=[('timestamp', -1)], limit=limit)


# ─── NOTIFICATION ─────────────────────────────────────────────────────────────

class Notification(MongoModel):
    collection_name = 'notifications'
    
    @classmethod
    def create(cls, user_id, title, message=None):
        """Create notification"""
        notification = {
            'user_id': user_id,
            'title': title,
            'message': message,
            'is_read': False,
            'created_at': datetime.utcnow()
        }
        return cls.insert_one(notification)
    
    @classmethod
    def find_by_user(cls, user_id, unread_only=False):
        """Find user's notifications"""
        filter_dict = {'user_id': user_id}
        if unread_only:
            filter_dict['is_read'] = False
        return cls.find(filter_dict, sort=[('created_at', -1)])
    
    @classmethod
    def mark_as_read(cls, notification_id):
        """Mark notification as read"""
        return cls.update_by_id(notification_id, {'is_read': True})


# ─── INSTITUTE SETTINGS ───────────────────────────────────────────────────────

class InstituteSetting(MongoModel):
    collection_name = 'institute_settings'
    
    @classmethod
    def get_settings(cls):
        """Get institute settings (singleton)"""
        settings = cls.find_one({})
        if not settings:
            # Create default settings
            default_settings = {
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
            cls.insert_one(default_settings)
            settings = default_settings
        return settings
    
    @classmethod
    def update_settings(cls, updates):
        """Update institute settings"""
        updates['updated_at'] = datetime.utcnow()
        settings = cls.find_one({})
        if settings:
            return cls.update_by_id(settings['id'], updates)
        else:
            return cls.insert_one(updates)


# ─── ASSIGNMENT & CERTIFICATE ─────────────────────────────────────────────────

class Assignment(MongoModel):
    collection_name = 'assignments'

class Certificate(MongoModel):
    collection_name = 'certificates'


# ─── FEE ACCOUNT (legacy) ─────────────────────────────────────────────────────

class FeeAccount(MongoModel):
    collection_name = 'fee_accounts'
