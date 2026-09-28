"""
Course management routes
"""
from flask import Blueprint, request, jsonify, session
from datetime import datetime
from models import db, Course, Batch, Student, ActivityLog
from routes.auth import login_required, role_required

courses_bp = Blueprint('courses', __name__)


@courses_bp.route('/', methods=['GET'])
@login_required
def get_courses():
    status_filter = request.args.get('status', '')
    query = Course.query
    if status_filter:
        query = query.filter_by(status=status_filter)
    courses = query.order_by(Course.name).all()
    return jsonify({'courses': [c.to_dict() for c in courses]}), 200


@courses_bp.route('/<int:course_id>', methods=['GET'])
@login_required
def get_course(course_id):
    course = Course.query.get_or_404(course_id)
    data = course.to_dict()
    data['batch_count'] = Batch.query.filter_by(course_id=course_id).count()
    data['student_count'] = Student.query.filter_by(course_id=course_id, is_active=True).count()
    return jsonify({'course': data}), 200


@courses_bp.route('/', methods=['POST'])
@login_required
@role_required('admin')
def create_course():
    data = request.get_json()
    if not data.get('name'):
        return jsonify({'error': 'Course name is required'}), 400
    if not data.get('code'):
        return jsonify({'error': 'Course code is required'}), 400
    if Course.query.filter_by(code=data['code'].upper().strip()).first():
        return jsonify({'error': 'Course code already exists'}), 400
    if Course.query.filter_by(name=data['name'].strip()).first():
        return jsonify({'error': 'Course name already exists'}), 400

    course = Course(
        name=data['name'].strip(),
        code=data['code'].upper().strip(),
        description=data.get('description', ''),
        duration=data.get('duration', ''),
        default_fee=float(data.get('default_fee', 0)),
        status=data.get('status', 'active')
    )
    db.session.add(course)
    db.session.add(ActivityLog(
        user_id=session['user_id'], action='COURSE_CREATED',
        details=f'Created course: {course.name} ({course.code})',
        status='SUCCESS', ip_address=request.remote_addr
    ))
    db.session.commit()
    return jsonify({'message': 'Course created', 'course': course.to_dict()}), 201


@courses_bp.route('/<int:course_id>', methods=['PUT'])
@login_required
@role_required('admin')
def update_course(course_id):
    course = Course.query.get_or_404(course_id)
    data = request.get_json()
    if 'name' in data:
        course.name = data['name'].strip()
    if 'code' in data:
        new_code = data['code'].upper().strip()
        existing = Course.query.filter_by(code=new_code).first()
        if existing and existing.id != course_id:
            return jsonify({'error': 'Course code already exists'}), 400
        course.code = new_code
    if 'description' in data:
        course.description = data['description']
    if 'duration' in data:
        course.duration = data['duration']
    if 'default_fee' in data:
        course.default_fee = float(data['default_fee'])
    if 'status' in data:
        course.status = data['status']
    db.session.add(ActivityLog(
        user_id=session['user_id'], action='COURSE_UPDATED',
        details=f'Updated course: {course.name}', status='SUCCESS',
        ip_address=request.remote_addr
    ))
    db.session.commit()
    return jsonify({'message': 'Course updated', 'course': course.to_dict()}), 200


@courses_bp.route('/<int:course_id>', methods=['DELETE'])
@login_required
@role_required('admin')
def delete_course(course_id):
    course = Course.query.get_or_404(course_id)
    # Archive instead of delete if students exist
    student_count = Student.query.filter_by(course_id=course_id).count()
    if student_count > 0:
        course.status = 'archived'
        db.session.commit()
        return jsonify({'message': f'Course archived (has {student_count} students)'}), 200
    db.session.delete(course)
    db.session.add(ActivityLog(
        user_id=session['user_id'], action='COURSE_DELETED',
        details=f'Deleted course: {course.name}', status='SUCCESS',
        ip_address=request.remote_addr
    ))
    db.session.commit()
    return jsonify({'message': 'Course deleted'}), 200
