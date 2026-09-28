"""
Batch management routes
"""
from flask import Blueprint, request, jsonify, session
from datetime import datetime
from models import db, Batch, Course, Student, Attendance, ActivityLog
from routes.auth import login_required, role_required

batches_bp = Blueprint('batches', __name__)


@batches_bp.route('/', methods=['GET'])
@login_required
def get_batches():
    status_filter = request.args.get('status', '')
    course_id = request.args.get('course_id', type=int)
    query = Batch.query
    if status_filter:
        query = query.filter_by(status=status_filter)
    if course_id:
        query = query.filter_by(course_id=course_id)
    batches = query.order_by(Batch.name).all()
    result = []
    for b in batches:
        d = b.to_dict()
        d['student_count'] = Student.query.filter_by(batch_id=b.id, is_active=True).count()
        result.append(d)
    return jsonify({'batches': result}), 200


@batches_bp.route('/<int:batch_id>', methods=['GET'])
@login_required
def get_batch(batch_id):
    batch = Batch.query.get_or_404(batch_id)
    data = batch.to_dict()
    students = Student.query.filter_by(batch_id=batch_id, is_active=True).all()
    data['students'] = [s.to_dict() for s in students]
    data['student_count'] = len(students)
    return jsonify({'batch': data}), 200


@batches_bp.route('/', methods=['POST'])
@login_required
@role_required('admin')
def create_batch():
    data = request.get_json()
    if not data.get('name'):
        return jsonify({'error': 'Batch name is required'}), 400
    if not data.get('code'):
        return jsonify({'error': 'Batch code is required'}), 400
    if Batch.query.filter_by(code=data['code'].upper().strip()).first():
        return jsonify({'error': 'Batch code already exists'}), 400

    batch = Batch(
        name=data['name'].strip(),
        code=data['code'].upper().strip(),
        course_id=data.get('course_id'),
        faculty=data.get('faculty', ''),
        start_date=datetime.fromisoformat(data['start_date']).date() if data.get('start_date') else None,
        end_date=datetime.fromisoformat(data['end_date']).date() if data.get('end_date') else None,
        start_time=data.get('start_time', ''),
        end_time=data.get('end_time', ''),
        schedule=data.get('schedule', ''),
        max_students=int(data['max_students']) if data.get('max_students') else None,
        status=data.get('status', 'active')
    )
    db.session.add(batch)
    db.session.add(ActivityLog(
        user_id=session['user_id'], action='BATCH_CREATED',
        details=f'Created batch: {batch.name} ({batch.code})',
        status='SUCCESS', ip_address=request.remote_addr
    ))
    db.session.commit()
    return jsonify({'message': 'Batch created', 'batch': batch.to_dict()}), 201


@batches_bp.route('/<int:batch_id>', methods=['PUT'])
@login_required
@role_required('admin')
def update_batch(batch_id):
    batch = Batch.query.get_or_404(batch_id)
    data = request.get_json()
    if 'name' in data:
        batch.name = data['name'].strip()
    if 'code' in data:
        new_code = data['code'].upper().strip()
        existing = Batch.query.filter_by(code=new_code).first()
        if existing and existing.id != batch_id:
            return jsonify({'error': 'Batch code already exists'}), 400
        batch.code = new_code
    if 'course_id' in data:
        batch.course_id = data['course_id']
    if 'faculty' in data:
        batch.faculty = data['faculty']
    if 'start_date' in data and data['start_date']:
        batch.start_date = datetime.fromisoformat(data['start_date']).date()
    if 'end_date' in data and data['end_date']:
        batch.end_date = datetime.fromisoformat(data['end_date']).date()
    if 'start_time' in data:
        batch.start_time = data['start_time']
    if 'end_time' in data:
        batch.end_time = data['end_time']
    if 'schedule' in data:
        batch.schedule = data['schedule']
    if 'max_students' in data:
        batch.max_students = int(data['max_students']) if data['max_students'] else None
    if 'status' in data:
        batch.status = data['status']
    db.session.add(ActivityLog(
        user_id=session['user_id'], action='BATCH_UPDATED',
        details=f'Updated batch: {batch.name}', status='SUCCESS',
        ip_address=request.remote_addr
    ))
    db.session.commit()
    return jsonify({'message': 'Batch updated', 'batch': batch.to_dict()}), 200


@batches_bp.route('/<int:batch_id>', methods=['DELETE'])
@login_required
@role_required('admin')
def delete_batch(batch_id):
    batch = Batch.query.get_or_404(batch_id)
    student_count = Student.query.filter_by(batch_id=batch_id).count()
    if student_count > 0:
        batch.status = 'archived'
        db.session.commit()
        return jsonify({'message': f'Batch archived ({student_count} students assigned)'}), 200
    db.session.delete(batch)
    db.session.commit()
    return jsonify({'message': 'Batch deleted'}), 200


@batches_bp.route('/<int:batch_id>/students', methods=['POST'])
@login_required
@role_required('admin')
def add_student_to_batch(batch_id):
    batch = Batch.query.get_or_404(batch_id)
    data = request.get_json()
    student = Student.query.get_or_404(data.get('student_id'))
    old_batch = student.batch_id
    student.batch_id = batch_id
    student.batch = batch.name
    db.session.add(ActivityLog(
        user_id=session['user_id'], action='STUDENT_MOVED_BATCH',
        details=f'Moved {student.first_name} {student.last_name} to batch {batch.name}',
        status='SUCCESS', ip_address=request.remote_addr
    ))
    db.session.commit()
    return jsonify({'message': f'Student added to {batch.name}'}), 200


@batches_bp.route('/<int:batch_id>/students/<int:student_id>', methods=['DELETE'])
@login_required
@role_required('admin')
def remove_student_from_batch(batch_id, student_id):
    student = Student.query.get_or_404(student_id)
    if student.batch_id != batch_id:
        return jsonify({'error': 'Student is not in this batch'}), 400
    student.batch_id = None
    student.batch = None
    db.session.add(ActivityLog(
        user_id=session['user_id'], action='STUDENT_REMOVED_BATCH',
        details=f'Removed {student.first_name} {student.last_name} from batch',
        status='SUCCESS', ip_address=request.remote_addr
    ))
    db.session.commit()
    return jsonify({'message': 'Student removed from batch'}), 200
