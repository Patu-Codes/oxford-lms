"""
Database models for Oxford LMS
"""
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import hashlib

db = SQLAlchemy()


# ─── USER ─────────────────────────────────────────────────────────────────────

class User(db.Model):
    __tablename__ = 'users'
    id           = db.Column(db.Integer, primary_key=True)
    username     = db.Column(db.String(50), unique=True, nullable=False, index=True)
    password     = db.Column(db.String(255), nullable=False)
    role         = db.Column(db.String(20), nullable=False)  # admin, faculty, student
    email        = db.Column(db.String(100))
    full_name    = db.Column(db.String(100))
    profile_image = db.Column(db.String(255))
    created_at   = db.Column(db.DateTime, default=datetime.utcnow)
    last_login   = db.Column(db.DateTime)
    is_active    = db.Column(db.Boolean, default=True)

    notes        = db.relationship('Note', back_populates='uploader', lazy='dynamic')
    activities   = db.relationship('ActivityLog', back_populates='user', lazy='dynamic')
    notifications = db.relationship('Notification', back_populates='user', lazy='dynamic')

    def set_password(self, password):
        self.password = hashlib.sha256(password.encode()).hexdigest()

    def check_password(self, password):
        return self.password == hashlib.sha256(password.encode()).hexdigest()

    def to_dict(self):
        return {
            'id': self.id, 'username': self.username, 'role': self.role,
            'email': self.email, 'full_name': self.full_name,
            'profile_image': self.profile_image,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_login': self.last_login.isoformat() if self.last_login else None,
            'is_active': self.is_active
        }


# ─── COURSE ───────────────────────────────────────────────────────────────────

class Course(db.Model):
    __tablename__ = 'courses'
    id          = db.Column(db.Integer, primary_key=True)
    name        = db.Column(db.String(100), unique=True, nullable=False)
    code        = db.Column(db.String(20), unique=True)
    description = db.Column(db.Text)
    duration    = db.Column(db.String(50))
    default_fee = db.Column(db.Float, default=0)
    status      = db.Column(db.String(20), default='active')   # active, inactive, archived
    created_at  = db.Column(db.DateTime, default=datetime.utcnow)

    batches     = db.relationship('Batch', back_populates='course', lazy='dynamic')
    students    = db.relationship('Student', back_populates='course_rel', lazy='dynamic')
    notes       = db.relationship('Note', back_populates='course_rel', lazy='dynamic')

    def to_dict(self):
        return {
            'id': self.id, 'name': self.name, 'code': self.code,
            'description': self.description, 'duration': self.duration,
            'default_fee': self.default_fee, 'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


# ─── BATCH ────────────────────────────────────────────────────────────────────

class Batch(db.Model):
    __tablename__ = 'batches'
    id           = db.Column(db.Integer, primary_key=True)
    name         = db.Column(db.String(100), nullable=False)
    code         = db.Column(db.String(50), unique=True)
    course_id    = db.Column(db.Integer, db.ForeignKey('courses.id'))
    faculty      = db.Column(db.String(100))
    start_date   = db.Column(db.Date)
    end_date     = db.Column(db.Date)
    start_time   = db.Column(db.String(10))
    end_time     = db.Column(db.String(10))
    schedule     = db.Column(db.String(100))   # e.g. "Mon-Fri", "Mon,Wed,Fri"
    max_students = db.Column(db.Integer)
    status       = db.Column(db.String(20), default='active')  # active, completed, archived
    created_at   = db.Column(db.DateTime, default=datetime.utcnow)

    course       = db.relationship('Course', back_populates='batches')
    students     = db.relationship('Student', back_populates='batch_rel', lazy='dynamic')
    attendance_records = db.relationship('Attendance', back_populates='batch', lazy='dynamic')

    def to_dict(self):
        course_name = self.course.name if self.course else None
        course_code = self.course.code if self.course else None
        return {
            'id': self.id, 'name': self.name, 'code': self.code,
            'course_id': self.course_id, 'course_name': course_name,
            'course_code': course_code, 'faculty': self.faculty,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'start_time': self.start_time, 'end_time': self.end_time,
            'schedule': self.schedule, 'max_students': self.max_students,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


# ─── STUDENT ──────────────────────────────────────────────────────────────────

class Student(db.Model):
    __tablename__ = 'students'
    id              = db.Column(db.Integer, primary_key=True)
    user_id         = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True)
    student_id      = db.Column(db.String(50), unique=True, nullable=False, index=True)
    first_name      = db.Column(db.String(100), nullable=False)
    last_name       = db.Column(db.String(100), nullable=False)
    date_of_birth   = db.Column(db.Date)
    gender          = db.Column(db.String(10))
    email           = db.Column(db.String(100))
    phone           = db.Column(db.String(20))
    address         = db.Column(db.Text)
    # Relationships stored as both FK (integrity) and text (display)
    course_id       = db.Column(db.Integer, db.ForeignKey('courses.id'))
    course          = db.Column(db.String(100))   # denormalized for display
    batch_id        = db.Column(db.Integer, db.ForeignKey('batches.id'))
    batch           = db.Column(db.String(100))   # denormalized for display
    enrollment_date = db.Column(db.Date)
    joining_date    = db.Column(db.Date)
    profile_image   = db.Column(db.String(255))
    guardian_name   = db.Column(db.String(100))
    guardian_phone  = db.Column(db.String(20))
    status          = db.Column(db.String(20), default='active')  # active, completed, on_hold, dropped
    is_active       = db.Column(db.Boolean, default=True)
    # Fee fields
    total_fee       = db.Column(db.Float)          # overrides course default_fee if set
    fee_remarks     = db.Column(db.Text)

    course_rel      = db.relationship('Course', back_populates='students')
    batch_rel       = db.relationship('Batch', back_populates='students')
    attendance      = db.relationship('Attendance', back_populates='student', lazy='dynamic')
    fee_payments    = db.relationship('FeePayment', back_populates='student', lazy='dynamic')
    fee_account     = db.relationship('StudentFeeAccount', back_populates='student',
                                      uselist=False, cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id, 'user_id': self.user_id,
            'student_id': self.student_id,
            'first_name': self.first_name, 'last_name': self.last_name,
            'full_name': f"{self.first_name} {self.last_name}",
            'date_of_birth': self.date_of_birth.isoformat() if self.date_of_birth else None,
            'gender': self.gender, 'email': self.email, 'phone': self.phone,
            'address': self.address, 'course': self.course, 'course_id': self.course_id,
            'batch': self.batch, 'batch_id': self.batch_id,
            'enrollment_date': self.enrollment_date.isoformat() if self.enrollment_date else None,
            'joining_date': self.joining_date.isoformat() if self.joining_date else None,
            'profile_image': self.profile_image,
            'guardian_name': self.guardian_name, 'guardian_phone': self.guardian_phone,
            'status': self.status, 'is_active': self.is_active,
            'total_fee': self.total_fee, 'fee_remarks': self.fee_remarks
        }


# ─── STUDENT FEE ACCOUNT ──────────────────────────────────────────────────────

class StudentFeeAccount(db.Model):
    """Per-student fee configuration — total fee, payment plan"""
    __tablename__ = 'student_fee_accounts'
    id                  = db.Column(db.Integer, primary_key=True)
    student_id          = db.Column(db.Integer, db.ForeignKey('students.id'), unique=True, nullable=False)
    total_fee           = db.Column(db.Float, nullable=False, default=0)
    installment_amount  = db.Column(db.Float)
    installment_freq    = db.Column(db.String(20))  # monthly, quarterly, custom
    next_due_date       = db.Column(db.Date)
    remarks             = db.Column(db.Text)
    created_at          = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at          = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    student             = db.relationship('Student', back_populates='fee_account')

    def to_dict(self):
        return {
            'id': self.id, 'student_id': self.student_id,
            'total_fee': self.total_fee,
            'installment_amount': self.installment_amount,
            'installment_freq': self.installment_freq,
            'next_due_date': self.next_due_date.isoformat() if self.next_due_date else None,
            'remarks': self.remarks
        }


# ─── FEE PAYMENT ──────────────────────────────────────────────────────────────

class FeePayment(db.Model):
    __tablename__ = 'fee_payments'
    id             = db.Column(db.Integer, primary_key=True)
    student_id     = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    course_id      = db.Column(db.Integer, db.ForeignKey('courses.id'))
    batch_id       = db.Column(db.Integer, db.ForeignKey('batches.id'))
    amount         = db.Column(db.Float, nullable=False)
    payment_date   = db.Column(db.Date, nullable=False, index=True)
    payment_mode   = db.Column(db.String(50))   # cash, upi, bank_transfer, cheque, other
    transaction_id = db.Column(db.String(100))
    receipt_number = db.Column(db.String(50), unique=True)
    remarks        = db.Column(db.Text)
    collected_by   = db.Column(db.Integer, db.ForeignKey('users.id'))
    # Snapshot fields — stored at time of payment, never change if settings change
    institute_name = db.Column(db.String(100))
    created_at     = db.Column(db.DateTime, default=datetime.utcnow)

    student        = db.relationship('Student', back_populates='fee_payments')

    def to_dict(self):
        return {
            'id': self.id, 'student_id': self.student_id,
            'course_id': self.course_id, 'batch_id': self.batch_id,
            'amount': self.amount,
            'payment_date': self.payment_date.isoformat(),
            'payment_mode': self.payment_mode,
            'transaction_id': self.transaction_id,
            'receipt_number': self.receipt_number,
            'remarks': self.remarks,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


# ─── FEE ACCOUNT (course-level structure — kept for backwards compat) ─────────

class FeeAccount(db.Model):
    __tablename__ = 'fee_accounts'
    id          = db.Column(db.Integer, primary_key=True)
    course      = db.Column(db.String(100), nullable=False)
    batch       = db.Column(db.String(50))
    total_fee   = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text)
    created_at  = db.Column(db.DateTime, default=datetime.utcnow)


# ─── ATTENDANCE ───────────────────────────────────────────────────────────────

class Attendance(db.Model):
    __tablename__ = 'attendance'
    id         = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    batch_id   = db.Column(db.Integer, db.ForeignKey('batches.id'))
    date       = db.Column(db.Date, nullable=False, index=True)
    status     = db.Column(db.String(10), nullable=False)  # present, absent, late, excused
    remarks    = db.Column(db.Text)
    marked_by  = db.Column(db.Integer, db.ForeignKey('users.id'))
    marked_at  = db.Column(db.DateTime, default=datetime.utcnow)

    student    = db.relationship('Student', back_populates='attendance')
    batch      = db.relationship('Batch', back_populates='attendance_records')

    __table_args__ = (db.UniqueConstraint('student_id', 'date', name='unique_attendance'),)


# ─── NOTE ─────────────────────────────────────────────────────────────────────

class Note(db.Model):
    __tablename__ = 'notes'
    id              = db.Column(db.Integer, primary_key=True)
    title           = db.Column(db.String(255), nullable=False)
    description     = db.Column(db.Text)
    category        = db.Column(db.String(50))
    course_id       = db.Column(db.Integer, db.ForeignKey('courses.id'))
    batch_id        = db.Column(db.Integer, db.ForeignKey('batches.id'))
    file_path       = db.Column(db.String(500), nullable=False)
    file_type       = db.Column(db.String(20))
    file_size       = db.Column(db.Integer)
    uploaded_by     = db.Column(db.Integer, db.ForeignKey('users.id'))
    uploaded_at     = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    visibility      = db.Column(db.String(20), default='all')  # all, students, admin
    views           = db.Column(db.Integer, default=0)
    downloads       = db.Column(db.Integer, default=0)
    tags            = db.Column(db.String(500))
    is_downloadable = db.Column(db.Boolean, default=False)  # default: View Only

    uploader    = db.relationship('User', back_populates='notes')
    favorites   = db.relationship('Favorite', back_populates='note', cascade='all, delete-orphan')
    course_rel  = db.relationship('Course', back_populates='notes')

    def to_dict(self):
        # NOTE: file_path is intentionally NOT exposed here.
        # File serving goes through authenticated /api/notes/<id>/view and /download only.
        return {
            'id': self.id, 'title': self.title, 'description': self.description,
            'category': self.category,
            'course_id': self.course_id,
            'course_name': self.course_rel.name if self.course_rel else None,
            'batch_id': self.batch_id,
            'file_type': self.file_type,
            'file_size': self.file_size,
            'uploaded_by': self.uploaded_by,
            'uploader_name': self.uploader.full_name if self.uploader else 'Admin',
            'uploaded_at': self.uploaded_at.isoformat() if self.uploaded_at else None,
            'visibility': self.visibility, 'views': self.views, 'downloads': self.downloads,
            'tags': self.tags, 'is_downloadable': self.is_downloadable
        }


# ─── FAVORITE ─────────────────────────────────────────────────────────────────

class Favorite(db.Model):
    __tablename__ = 'favorites'
    id         = db.Column(db.Integer, primary_key=True)
    user_id    = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    note_id    = db.Column(db.Integer, db.ForeignKey('notes.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    note       = db.relationship('Note', back_populates='favorites')
    __table_args__ = (db.UniqueConstraint('user_id', 'note_id', name='unique_favorite'),)


# ─── ACTIVITY LOG ─────────────────────────────────────────────────────────────

class ActivityLog(db.Model):
    __tablename__ = 'activity_logs'
    id         = db.Column(db.Integer, primary_key=True)
    user_id    = db.Column(db.Integer, db.ForeignKey('users.id'))
    action     = db.Column(db.String(100), nullable=False)
    details    = db.Column(db.Text)
    status     = db.Column(db.String(20), default='SUCCESS')
    ip_address = db.Column(db.String(50))
    timestamp  = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    user       = db.relationship('User', back_populates='activities')


# ─── NOTIFICATION ─────────────────────────────────────────────────────────────

class Notification(db.Model):
    __tablename__ = 'notifications'
    id         = db.Column(db.Integer, primary_key=True)
    user_id    = db.Column(db.Integer, db.ForeignKey('users.id'))
    title      = db.Column(db.String(255), nullable=False)
    message    = db.Column(db.Text)
    is_read    = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    user       = db.relationship('User', back_populates='notifications')


# ─── INSTITUTE SETTINGS ───────────────────────────────────────────────────────

class InstituteSetting(db.Model):
    __tablename__ = 'institute_settings'
    id                   = db.Column(db.Integer, primary_key=True)
    institute_name       = db.Column(db.String(100), default='Oxford LMS')
    institute_address    = db.Column(db.Text, default='')
    institute_phone      = db.Column(db.String(30), default='')
    institute_email      = db.Column(db.String(100), default='')
    institute_website    = db.Column(db.String(100), default='')
    receipt_prefix       = db.Column(db.String(20), default='OXLMS')
    receipt_footer       = db.Column(db.Text, default='Thank you for your payment.')
    authorized_signatory = db.Column(db.String(100), default='Administrator')
    currency_symbol      = db.Column(db.String(5), default='Rs.')
    updated_at           = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'institute_name': self.institute_name,
            'institute_address': self.institute_address,
            'institute_phone': self.institute_phone,
            'institute_email': self.institute_email,
            'institute_website': self.institute_website,
            'receipt_prefix': self.receipt_prefix,
            'receipt_footer': self.receipt_footer,
            'authorized_signatory': self.authorized_signatory,
            'currency_symbol': self.currency_symbol,
        }


# ─── ASSIGNMENT / CERTIFICATE (models kept, no active routes yet) ─────────────

class Assignment(db.Model):
    __tablename__ = 'assignments'
    id          = db.Column(db.Integer, primary_key=True)
    title       = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    course      = db.Column(db.String(100))
    batch       = db.Column(db.String(50))
    due_date    = db.Column(db.Date)
    file_path   = db.Column(db.String(500))
    created_by  = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at  = db.Column(db.DateTime, default=datetime.utcnow)


class Certificate(db.Model):
    __tablename__ = 'certificates'
    id                 = db.Column(db.Integer, primary_key=True)
    student_id         = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    certificate_type   = db.Column(db.String(100), nullable=False)
    certificate_number = db.Column(db.String(50), unique=True)
    issue_date         = db.Column(db.Date, nullable=False)
    file_path          = db.Column(db.String(500))
    issued_by          = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at         = db.Column(db.DateTime, default=datetime.utcnow)


# ─── DB INIT ──────────────────────────────────────────────────────────────────

def _migrate_columns():
    """Add new columns to existing tables without losing data."""
    from sqlalchemy import text, inspect
    insp = inspect(db.engine)

    def col_exists(table, col):
        return any(c['name'] == col for c in insp.get_columns(table))

    migrations = [
        # courses
        ("courses", "code",        "ALTER TABLE courses ADD COLUMN code VARCHAR(20)"),
        ("courses", "default_fee", "ALTER TABLE courses ADD COLUMN default_fee FLOAT DEFAULT 0"),
        ("courses", "status",      "ALTER TABLE courses ADD COLUMN status VARCHAR(20) DEFAULT 'active'"),
        # batches
        ("batches", "code",         "ALTER TABLE batches ADD COLUMN code VARCHAR(50)"),
        ("batches", "course_id",    "ALTER TABLE batches ADD COLUMN course_id INTEGER"),
        ("batches", "faculty",      "ALTER TABLE batches ADD COLUMN faculty VARCHAR(100)"),
        ("batches", "start_time",   "ALTER TABLE batches ADD COLUMN start_time VARCHAR(10)"),
        ("batches", "end_time",     "ALTER TABLE batches ADD COLUMN end_time VARCHAR(10)"),
        ("batches", "schedule",     "ALTER TABLE batches ADD COLUMN schedule VARCHAR(100)"),
        ("batches", "max_students", "ALTER TABLE batches ADD COLUMN max_students INTEGER"),
        ("batches", "status",       "ALTER TABLE batches ADD COLUMN status VARCHAR(20) DEFAULT 'active'"),
        # students
        ("students", "course_id",     "ALTER TABLE students ADD COLUMN course_id INTEGER"),
        ("students", "batch_id",      "ALTER TABLE students ADD COLUMN batch_id INTEGER"),
        ("students", "status",        "ALTER TABLE students ADD COLUMN status VARCHAR(20) DEFAULT 'active'"),
        ("students", "joining_date",  "ALTER TABLE students ADD COLUMN joining_date DATE"),
        ("students", "total_fee",     "ALTER TABLE students ADD COLUMN total_fee FLOAT"),
        ("students", "fee_remarks",   "ALTER TABLE students ADD COLUMN fee_remarks TEXT"),
        # notes
        ("notes", "course_id", "ALTER TABLE notes ADD COLUMN course_id INTEGER"),
        ("notes", "batch_id",  "ALTER TABLE notes ADD COLUMN batch_id INTEGER"),
        ("notes", "is_downloadable", "ALTER TABLE notes ADD COLUMN is_downloadable BOOLEAN DEFAULT 0"),
        # attendance
        ("attendance", "batch_id", "ALTER TABLE attendance ADD COLUMN batch_id INTEGER"),
        # fee_payments
        ("fee_payments", "course_id",      "ALTER TABLE fee_payments ADD COLUMN course_id INTEGER"),
        ("fee_payments", "batch_id",       "ALTER TABLE fee_payments ADD COLUMN batch_id INTEGER"),
        ("fee_payments", "institute_name", "ALTER TABLE fee_payments ADD COLUMN institute_name VARCHAR(100)"),
    ]

    for table, col, sql in migrations:
        try:
            if insp.has_table(table) and not col_exists(table, col):
                db.session.execute(text(sql))
                db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"Migration skipped ({table}.{col}): {e}")


def init_db():
    db.create_all()
    _migrate_columns()

    admin = User.query.filter_by(username='admin').first()
    if not admin:
        admin = User(username='admin', role='admin',
                     email='admin@oxford.edu', full_name='System Administrator')
        admin.set_password('admin123')
        db.session.add(admin)

    # Default courses
    default_courses = [
        ('Python Programming', 'PY', '6 Months', 30000),
        ('Data Science', 'DS', '9 Months', 50000),
        ('Web Development', 'WD', '6 Months', 35000),
        ('Machine Learning', 'ML', '12 Months', 70000),
        ('Cloud Computing', 'CC', '12 Months', 70000),
    ]
    for cname, ccode, cdur, cfee in default_courses:
        if not Course.query.filter_by(name=cname).first():
            db.session.add(Course(name=cname, code=ccode, duration=cdur,
                                  default_fee=cfee, status='active'))

    # Default institute settings
    if not InstituteSetting.query.first():
        db.session.add(InstituteSetting(
            institute_name='Oxford LMS',
            receipt_prefix='OXLMS',
            authorized_signatory='Administrator',
            currency_symbol='Rs.'
        ))

    db.session.commit()
    print("Oxford LMS database initialized.")
