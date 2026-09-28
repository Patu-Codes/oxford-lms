"""
Student management routes — Oxford LMS
"""
from flask import Blueprint, request, jsonify, session
from werkzeug.utils import secure_filename
from datetime import datetime
from pathlib import Path

from models import db, Student, User, Course, Batch, ActivityLog, StudentFeeAccount
from routes.auth import login_required, role_required
from config import Config

students_bp = Blueprint('students', __name__)


@students_bp.route('/', methods=['GET'])
@login_required
@role_required('admin')
def get_students():
    query_str  = request.args.get('query', '')
    course_id  = request.args.get('course_id', type=int)
    batch_id   = request.args.get('batch_id', type=int)
    status     = request.args.get('status', '')
    active_only = request.args.get('active', 'true').lower() == 'true'
    page       = int(request.args.get('page', 1))
    per_page   = int(request.args.get('per_page', 50))

    q = Student.query
    if query_str:
        q = q.filter(db.or_(
            Student.first_name.ilike(f'%{query_str}%'),
            Student.last_name.ilike(f'%{query_str}%'),
            Student.student_id.ilike(f'%{query_str}%'),
            Student.email.ilike(f'%{query_str}%'),
        ))
    if course_id:
        q = q.filter_by(course_id=course_id)
    if batch_id:
        q = q.filter_by(batch_id=batch_id)
    if status:
        q = q.filter_by(status=status)
    if active_only:
        q = q.filter_by(is_active=True)

    pagination = q.order_by(Student.first_name).paginate(page=page, per_page=per_page, error_out=False)
    return jsonify({
        'students': [s.to_dict() for s in pagination.items],
        'total': pagination.total, 'pages': pagination.pages, 'current_page': page
    }), 200


@students_bp.route('/<int:student_id>', methods=['GET'])
@login_required
def get_student(student_id):
    student = Student.query.get_or_404(student_id)
    user = User.query.get(session['user_id'])
    if user.role == 'student' and student.user_id != session['user_id']:
        return jsonify({'error': 'Access denied'}), 403
    return jsonify({'student': student.to_dict()}), 200


@students_bp.route('/', methods=['POST'])
@login_required
@role_required('admin')
def create_student():
    data = request.get_json()
    for field in ['student_id', 'first_name', 'last_name', 'email', 'password']:
        if not data.get(field):
            return jsonify({'error': f'{field.replace("_"," ").title()} is required'}), 400
    if len(data['password']) < 6:
        return jsonify({'error': 'Password must be at least 6 characters'}), 400
    if Student.query.filter_by(student_id=data['student_id']).first():
        return jsonify({'error': 'Student ID already exists'}), 400
    if Student.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already exists'}), 400
    if User.query.filter_by(username=data['student_id']).first():
        return jsonify({'error': 'Student ID already taken as username'}), 400

    # Resolve course/batch names from IDs if provided
    course_name = None
    batch_name  = None
    course_id   = data.get('course_id')
    batch_id    = data.get('batch_id')
    if course_id:
        c = Course.query.get(course_id)
        course_name = c.name if c else None
    elif data.get('course'):
        course_name = data['course']
    if batch_id:
        b = Batch.query.get(batch_id)
        batch_name = b.name if b else None
    elif data.get('batch'):
        batch_name = data['batch']

    user_account = User(username=data['student_id'], role='student',
                        email=data['email'],
                        full_name=f"{data['first_name']} {data['last_name']}")
    user_account.set_password(data['password'])
    db.session.add(user_account)
    db.session.flush()

    student = Student(
        user_id=user_account.id,
        student_id=data['student_id'],
        first_name=data['first_name'],
        last_name=data['last_name'],
        date_of_birth=datetime.fromisoformat(data['date_of_birth']).date() if data.get('date_of_birth') else None,
        gender=data.get('gender'),
        email=data['email'],
        phone=data.get('phone'),
        address=data.get('address'),
        course=course_name,
        course_id=course_id,
        batch=batch_name,
        batch_id=batch_id,
        enrollment_date=datetime.now().date(),
        joining_date=datetime.fromisoformat(data['joining_date']).date() if data.get('joining_date') else datetime.now().date(),
        guardian_name=data.get('guardian_name'),
        guardian_phone=data.get('guardian_phone'),
        status=data.get('status', 'active'),
        is_active=True,
    )
    db.session.add(student)
    db.session.flush()

    # Create fee account if total_fee provided
    total_fee = None
    if data.get('total_fee'):
        total_fee = float(data['total_fee'])
    elif course_id:
        c = Course.query.get(course_id)
        total_fee = c.default_fee if c else None

    if total_fee is not None:
        student.total_fee = total_fee
        fee_acc = StudentFeeAccount(
            student_id=student.id,
            total_fee=total_fee,
            installment_amount=float(data['installment_amount']) if data.get('installment_amount') else None,
            installment_freq=data.get('installment_freq'),
            next_due_date=datetime.fromisoformat(data['next_due_date']).date() if data.get('next_due_date') else None
        )
        db.session.add(fee_acc)

    db.session.add(ActivityLog(
        user_id=session['user_id'], action='STUDENT_CREATED',
        details=f'Created student: {student.first_name} {student.last_name} ({student.student_id})',
        status='SUCCESS', ip_address=request.remote_addr
    ))
    db.session.commit()
    return jsonify({'message': 'Student created', 'student': student.to_dict(),
                    'login_credentials': {'username': data['student_id']}}), 201


@students_bp.route('/<int:student_id>', methods=['PUT'])
@login_required
@role_required('admin')
def update_student(student_id):
    student = Student.query.get_or_404(student_id)
    data = request.get_json()

    for field in ['first_name', 'last_name', 'email', 'phone', 'address',
                  'gender', 'guardian_name', 'guardian_phone', 'status', 'fee_remarks']:
        if field in data:
            setattr(student, field, data[field])

    if 'date_of_birth' in data and data['date_of_birth']:
        student.date_of_birth = datetime.fromisoformat(data['date_of_birth']).date()
    if 'joining_date' in data and data['joining_date']:
        student.joining_date = datetime.fromisoformat(data['joining_date']).date()
    if 'course_id' in data:
        student.course_id = data['course_id']
        if data['course_id']:
            c = Course.query.get(data['course_id'])
            student.course = c.name if c else student.course
    if 'batch_id' in data:
        student.batch_id = data['batch_id']
        if data['batch_id']:
            b = Batch.query.get(data['batch_id'])
            student.batch = b.name if b else student.batch
    if 'is_active' in data:
        student.is_active = data['is_active']

    # Also update linked user full_name and email
    if student.user_id:
        u = User.query.get(student.user_id)
        if u:
            u.full_name = f"{student.first_name} {student.last_name}"
            if 'email' in data:
                u.email = data['email']

    db.session.add(ActivityLog(
        user_id=session['user_id'], action='STUDENT_UPDATED',
        details=f'Updated student: {student.first_name} {student.last_name}',
        status='SUCCESS', ip_address=request.remote_addr
    ))
    db.session.commit()
    return jsonify({'message': 'Student updated', 'student': student.to_dict()}), 200


@students_bp.route('/<int:student_id>', methods=['DELETE'])
@login_required
@role_required('admin')
def delete_student(student_id):
    student = Student.query.get_or_404(student_id)
    name = f"{student.first_name} {student.last_name}"
    if student.user_id:
        u = User.query.get(student.user_id)
        if u:
            db.session.delete(u)
    db.session.delete(student)
    db.session.add(ActivityLog(
        user_id=session['user_id'], action='STUDENT_DELETED',
        details=f'Deleted student: {name}', status='SUCCESS',
        ip_address=request.remote_addr
    ))
    db.session.commit()
    return jsonify({'message': 'Student deleted'}), 200


@students_bp.route('/<int:student_id>/profile-image', methods=['POST'])
@login_required
def upload_profile_image(student_id):
    student = Student.query.get_or_404(student_id)
    user = User.query.get(session['user_id'])
    if user.role == 'student' and student.user_id != session['user_id']:
        return jsonify({'error': 'Access denied'}), 403
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    file = request.files['file']
    ext = file.filename.rsplit('.', 1)[-1].lower()
    if ext not in {'png', 'jpg', 'jpeg'}:
        return jsonify({'error': 'Only PNG/JPG allowed'}), 400
    fname = secure_filename(f"{student.student_id}_profile.{ext}")
    upload_dir = Config.UPLOAD_FOLDER / 'images' / 'profiles'
    upload_dir.mkdir(parents=True, exist_ok=True)
    file.save(str(upload_dir / fname))
    student.profile_image = f"images/profiles/{fname}"
    if student.user_id:
        u = User.query.get(student.user_id)
        if u:
            u.profile_image = student.profile_image
    db.session.commit()
    return jsonify({'message': 'Image uploaded', 'profile_image': student.profile_image}), 200


# ─── HELPER ENDPOINTS ─────────────────────────────────────────────────────────

@students_bp.route('/courses', methods=['GET'])
@login_required
def get_courses():
    courses = Course.query.filter_by(status='active').order_by(Course.name).all()
    return jsonify({'courses': [c.to_dict() for c in courses]}), 200


@students_bp.route('/batches', methods=['GET'])
@login_required
def get_batches():
    course_id = request.args.get('course_id', type=int)
    q = Batch.query.filter_by(status='active')
    if course_id:
        q = q.filter_by(course_id=course_id)
    batches = q.order_by(Batch.name).all()
    return jsonify({'batches': [b.to_dict() for b in batches]}), 200
