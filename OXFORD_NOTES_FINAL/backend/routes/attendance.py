"""
Attendance routes — Oxford LMS (batch-based)
"""
from flask import Blueprint, request, jsonify, session
from datetime import datetime
from models import db, Attendance, Student, Batch, User, ActivityLog
from routes.auth import login_required, role_required

attendance_bp = Blueprint('attendance', __name__)


@attendance_bp.route('/', methods=['GET'])
@login_required
@role_required('admin')
def get_attendance():
    batch_id   = request.args.get('batch_id', type=int)
    student_id = request.args.get('student_id', type=int)
    date_from  = request.args.get('date_from')
    date_to    = request.args.get('date_to')
    status     = request.args.get('status')

    query = Attendance.query.join(Student)
    if batch_id:
        query = query.filter(Attendance.batch_id == batch_id)
    if student_id:
        query = query.filter(Attendance.student_id == student_id)
    if date_from:
        query = query.filter(Attendance.date >= datetime.fromisoformat(date_from).date())
    if date_to:
        query = query.filter(Attendance.date <= datetime.fromisoformat(date_to).date())
    if status:
        query = query.filter(Attendance.status == status)

    records = query.order_by(Attendance.date.desc()).all()
    return jsonify({'attendance': [{
        'id': r.id,
        'student_id': r.student_id,
        'student_name': f"{r.student.first_name} {r.student.last_name}",
        'student_number': r.student.student_id,
        'batch_id': r.batch_id,
        'date': r.date.isoformat(),
        'status': r.status,
        'remarks': r.remarks,
        'marked_at': r.marked_at.isoformat() if r.marked_at else None
    } for r in records]}), 200


@attendance_bp.route('/batch/<int:batch_id>/date/<string:date_str>', methods=['GET'])
@login_required
@role_required('admin')
def get_batch_attendance(batch_id, date_str):
    """Get attendance for a batch on a specific date, with student list."""
    batch = Batch.query.get_or_404(batch_id)
    date  = datetime.fromisoformat(date_str).date()
    students = Student.query.filter_by(batch_id=batch_id, is_active=True).all()
    att_map  = {a.student_id: a for a in Attendance.query.filter_by(batch_id=batch_id, date=date).all()}

    result = []
    for s in students:
        a = att_map.get(s.id)
        result.append({
            'student_id': s.id,
            'student_number': s.student_id,
            'student_name': f"{s.first_name} {s.last_name}",
            'status': a.status if a else None,
            'remarks': a.remarks if a else '',
            'attendance_id': a.id if a else None
        })
    return jsonify({
        'batch': batch.to_dict(),
        'date': date_str,
        'students': result
    }), 200


@attendance_bp.route('/mark', methods=['POST'])
@login_required
@role_required('admin')
def mark_attendance():
    data = request.get_json()
    date_str   = data.get('date')
    batch_id   = data.get('batch_id')
    records    = data.get('records', [])   # [{student_id, status, remarks}]

    if not date_str:
        return jsonify({'error': 'Date is required'}), 400
    if not records:
        return jsonify({'error': 'No records provided'}), 400

    date = datetime.fromisoformat(date_str).date()
    count = 0
    for rec in records:
        sid    = rec.get('student_id')
        status = rec.get('status', 'present')
        if status not in ('present', 'absent', 'late', 'excused'):
            status = 'absent'
        existing = Attendance.query.filter_by(student_id=sid, date=date).first()
        if existing:
            existing.status    = status
            existing.remarks   = rec.get('remarks', '')
            existing.batch_id  = batch_id
            existing.marked_by = session['user_id']
            existing.marked_at = datetime.utcnow()
        else:
            db.session.add(Attendance(
                student_id=sid, batch_id=batch_id, date=date,
                status=status, remarks=rec.get('remarks', ''),
                marked_by=session['user_id']
            ))
        count += 1

    db.session.add(ActivityLog(
        user_id=session['user_id'], action='ATTENDANCE_MARKED',
        details=f'Marked attendance for {count} student(s) on {date_str}',
        status='SUCCESS', ip_address=request.remote_addr
    ))
    db.session.commit()
    return jsonify({'message': f'Attendance saved for {count} students'}), 200


@attendance_bp.route('/student/<int:student_id>', methods=['GET'])
@login_required
def get_student_attendance(student_id):
    student  = Student.query.get_or_404(student_id)
    user     = User.query.get(session['user_id'])
    if user.role == 'student' and student.user_id != session['user_id']:
        return jsonify({'error': 'Access denied'}), 403

    date_from = request.args.get('date_from')
    date_to   = request.args.get('date_to')
    query = Attendance.query.filter_by(student_id=student_id)
    if date_from:
        query = query.filter(Attendance.date >= datetime.fromisoformat(date_from).date())
    if date_to:
        query = query.filter(Attendance.date <= datetime.fromisoformat(date_to).date())

    records  = query.order_by(Attendance.date.desc()).all()
    total    = len(records)
    present  = sum(1 for r in records if r.status == 'present')
    absent   = sum(1 for r in records if r.status == 'absent')
    late     = sum(1 for r in records if r.status == 'late')
    excused  = sum(1 for r in records if r.status == 'excused')
    pct      = round(present / total * 100, 1) if total > 0 else 0

    return jsonify({
        'student': student.to_dict(),
        'attendance': [{'id': r.id, 'date': r.date.isoformat(),
                        'status': r.status, 'remarks': r.remarks} for r in records],
        'statistics': {'total_days': total, 'present': present, 'absent': absent,
                       'late': late, 'excused': excused, 'percentage': pct}
    }), 200


@attendance_bp.route('/<int:att_id>', methods=['DELETE'])
@login_required
@role_required('admin')
def delete_attendance(att_id):
    a = Attendance.query.get_or_404(att_id)
    db.session.delete(a)
    db.session.commit()
    return jsonify({'message': 'Record deleted'}), 200
