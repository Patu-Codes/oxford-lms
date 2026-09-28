"""
Dashboard routes — Oxford LMS
"""
from flask import Blueprint, request, jsonify, session
from datetime import datetime, timedelta
from sqlalchemy import func

from models import (db, User, Note, Student, Attendance, FeePayment,
                    ActivityLog, Notification, Batch, Course, StudentFeeAccount)
from routes.auth import login_required

dashboard_bp = Blueprint('dashboard', __name__)


# ─── ADMIN DASHBOARD ──────────────────────────────────────────────────────────

def _admin_dashboard():
    today = datetime.now().date()

    # Top cards
    total_students   = Student.query.filter_by(is_active=True).count()
    active_batches   = Batch.query.filter_by(status='active').count()
    today_present    = Attendance.query.filter_by(date=today, status='present').count()
    today_total_att  = Attendance.query.filter_by(date=today).count()

    # Fee attention: students whose next_due_date is overdue or within 7 days
    upcoming_cutoff = today + timedelta(days=7)
    overdue_fee_students = (
        StudentFeeAccount.query
        .filter(StudentFeeAccount.next_due_date < today)
        .count()
    )
    upcoming_fee_students = (
        StudentFeeAccount.query
        .filter(StudentFeeAccount.next_due_date >= today,
                StudentFeeAccount.next_due_date <= upcoming_cutoff)
        .count()
    )

    # Today's batches
    todays_batches_q = Batch.query.filter_by(status='active').all()
    todays_batches = []
    for b in todays_batches_q:
        sc = Student.query.filter_by(batch_id=b.id, is_active=True).count()
        att_done = Attendance.query.filter_by(batch_id=b.id, date=today).count()
        todays_batches.append({
            'id': b.id, 'name': b.name, 'code': b.code,
            'course_name': b.course.name if b.course else 'N/A',
            'faculty': b.faculty or 'N/A',
            'start_time': b.start_time or '', 'end_time': b.end_time or '',
            'schedule': b.schedule or '',
            'student_count': sc,
            'attendance_marked': att_done > 0
        })

    # Fee attention list
    fee_attention = []
    overdue_accounts = (
        StudentFeeAccount.query
        .filter(StudentFeeAccount.next_due_date <= upcoming_cutoff)
        .order_by(StudentFeeAccount.next_due_date)
        .limit(10).all()
    )
    for acc in overdue_accounts:
        s = acc.student
        total_paid = db.session.query(func.sum(FeePayment.amount)).filter_by(
            student_id=s.id).scalar() or 0
        remaining = acc.total_fee - total_paid
        if remaining <= 0:
            continue
        status = 'overdue' if acc.next_due_date and acc.next_due_date < today else 'due_soon'
        fee_attention.append({
            'student_id': s.student_id,
            'student_name': f"{s.first_name} {s.last_name}",
            'course': s.course or 'N/A',
            'batch': s.batch or 'N/A',
            'remaining': remaining,
            'next_due_date': acc.next_due_date.isoformat() if acc.next_due_date else None,
            'installment_amount': acc.installment_amount,
            'status': status
        })

    # Recent notes
    recent_notes = Note.query.order_by(Note.uploaded_at.desc()).limit(6).all()

    return jsonify({
        'role': 'admin',
        'overview': {
            'total_students': total_students,
            'active_batches': active_batches,
            'today_present': today_present,
            'today_total': today_total_att,
            'overdue_fee_students': overdue_fee_students,
            'upcoming_fee_students': upcoming_fee_students,
        },
        'todays_batches': todays_batches,
        'fee_attention': fee_attention,
        'recent_notes': [n.to_dict() for n in recent_notes],
    }), 200


# ─── STUDENT DASHBOARD ────────────────────────────────────────────────────────

def _student_dashboard():
    user_id = session.get('user_id')
    student = Student.query.filter_by(user_id=user_id).first()
    if not student:
        return jsonify({'error': 'Student profile not found'}), 404

    today = datetime.now().date()
    thirty_ago = today - timedelta(days=30)

    # Attendance last 30 days
    att_records = Attendance.query.filter(
        Attendance.student_id == student.id,
        Attendance.date >= thirty_ago
    ).all()
    total_days  = len(att_records)
    present     = sum(1 for r in att_records if r.status == 'present')
    att_pct     = round(present / total_days * 100, 1) if total_days > 0 else 0

    # Fee summary
    fee_acct = student.fee_account
    total_fee = fee_acct.total_fee if fee_acct else (student.total_fee or 0)
    total_paid = db.session.query(func.sum(FeePayment.amount)).filter_by(
        student_id=student.id).scalar() or 0
    remaining  = total_fee - total_paid

    # Recent notes for student's course/batch
    notes_q = Note.query.filter(Note.visibility.in_(['all', 'students']))
    if student.course_id:
        notes_q = notes_q.filter(
            db.or_(Note.course_id == student.course_id, Note.course_id == None)
        )
    recent_notes = notes_q.order_by(Note.uploaded_at.desc()).limit(5).all()

    return jsonify({
        'role': 'student',
        'student': student.to_dict(),
        'attendance': {'total_days': total_days, 'present': present, 'percentage': att_pct},
        'fees': {
            'total_fee': total_fee,
            'total_paid': float(total_paid),
            'remaining': float(remaining),
            'next_due_date': fee_acct.next_due_date.isoformat() if (fee_acct and fee_acct.next_due_date) else None,
            'installment_amount': fee_acct.installment_amount if fee_acct else None
        },
        'recent_notes': [n.to_dict() for n in recent_notes],
    }), 200


@dashboard_bp.route('/', methods=['GET'])
@login_required
def get_dashboard():
    user = User.query.get(session['user_id'])
    if user.role == 'student':
        return _student_dashboard()
    return _admin_dashboard()


# ─── NOTIFICATIONS ────────────────────────────────────────────────────────────

@dashboard_bp.route('/notifications', methods=['GET'])
@login_required
def get_notifications():
    user_id = session.get('user_id')
    unread_only = request.args.get('unread', 'false').lower() == 'true'
    query = Notification.query.filter_by(user_id=user_id)
    if unread_only:
        query = query.filter_by(is_read=False)
    notifications = query.order_by(Notification.created_at.desc()).limit(20).all()
    unread_count = Notification.query.filter_by(user_id=user_id, is_read=False).count()
    return jsonify({
        'notifications': [{'id': n.id, 'title': n.title, 'message': n.message,
                           'is_read': n.is_read, 'created_at': n.created_at.isoformat()}
                          for n in notifications],
        'unread_count': unread_count
    }), 200


@dashboard_bp.route('/notifications/<int:nid>/read', methods=['POST'])
@login_required
def mark_read(nid):
    n = Notification.query.get_or_404(nid)
    if n.user_id != session['user_id']:
        return jsonify({'error': 'Access denied'}), 403
    n.is_read = True
    db.session.commit()
    return jsonify({'message': 'Marked as read'}), 200


@dashboard_bp.route('/notifications/mark-all-read', methods=['POST'])
@login_required
def mark_all_read():
    Notification.query.filter_by(user_id=session['user_id'], is_read=False).update({'is_read': True})
    db.session.commit()
    return jsonify({'message': 'All marked as read'}), 200


# ─── ACTIVITY ─────────────────────────────────────────────────────────────────

@dashboard_bp.route('/activity', methods=['GET'])
@login_required
def get_activity():
    user_id = session.get('user_id')
    user = User.query.get(user_id)
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 50))

    query = ActivityLog.query
    if user.role == 'student':
        query = query.filter_by(user_id=user_id)

    pagination = query.order_by(ActivityLog.timestamp.desc()).paginate(
        page=page, per_page=per_page, error_out=False)

    return jsonify({
        'activities': [{
            'id': a.id,
            'user': a.user.username if a.user else 'System',
            'user_name': a.user.full_name if a.user else 'System',
            'action': a.action, 'details': a.details,
            'status': a.status,
            'timestamp': a.timestamp.isoformat()
        } for a in pagination.items],
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': page
    }), 200
