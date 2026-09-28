"""
Reports and exports routes
"""
from flask import Blueprint, request, jsonify, session, send_file
from datetime import datetime
from sqlalchemy import func
import csv
import io

from models import db, Student, Note, Attendance, FeePayment, ActivityLog
from routes.auth import login_required, role_required

reports_bp = Blueprint('reports', __name__)

@reports_bp.route('/export/students', methods=['GET'])
@login_required
@role_required('admin', 'librarian')
def export_students():
    """Export students list to CSV"""
    students = Student.query.filter_by(is_active=True).all()
    
    # Create CSV in memory
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Headers
    writer.writerow([
        'Student ID', 'First Name', 'Last Name', 'Email', 'Phone',
        'Course', 'Batch', 'Enrollment Date', 'Guardian Name', 'Guardian Phone'
    ])
    
    # Data
    for student in students:
        writer.writerow([
            student.student_id,
            student.first_name,
            student.last_name,
            student.email,
            student.phone,
            student.course,
            student.batch,
            student.enrollment_date.isoformat() if student.enrollment_date else '',
            student.guardian_name,
            student.guardian_phone
        ])
    
    # Prepare response
    output.seek(0)
    return send_file(
        io.BytesIO(output.getvalue().encode('utf-8')),
        mimetype='text/csv',
        as_attachment=True,
        download_name=f'students_{datetime.now().strftime("%Y%m%d")}.csv'
    )

@reports_bp.route('/export/attendance', methods=['GET'])
@login_required
@role_required('admin', 'librarian')
def export_attendance():
    """Export attendance report to CSV"""
    date_from = request.args.get('date_from')
    date_to = request.args.get('date_to')
    
    if not date_from or not date_to:
        return jsonify({'error': 'Date range required'}), 400
    
    from_date = datetime.fromisoformat(date_from).date()
    to_date = datetime.fromisoformat(date_to).date()
    
    # Get attendance records
    records = Attendance.query.join(Student).filter(
        Attendance.date >= from_date,
        Attendance.date <= to_date
    ).order_by(Attendance.date.desc(), Student.first_name).all()
    
    # Create CSV
    output = io.StringIO()
    writer = csv.writer(output)
    
    writer.writerow([
        'Date', 'Student ID', 'Student Name', 'Course', 'Batch', 'Status', 'Remarks'
    ])
    
    for record in records:
        writer.writerow([
            record.date.isoformat(),
            record.student.student_id,
            f"{record.student.first_name} {record.student.last_name}",
            record.student.course,
            record.student.batch,
            record.status,
            record.remarks
        ])
    
    output.seek(0)
    return send_file(
        io.BytesIO(output.getvalue().encode('utf-8')),
        mimetype='text/csv',
        as_attachment=True,
        download_name=f'attendance_{from_date}_{to_date}.csv'
    )

@reports_bp.route('/export/fees', methods=['GET'])
@login_required
@role_required('admin', 'librarian')
def export_fees():
    """Export fee payments to CSV"""
    date_from = request.args.get('date_from')
    date_to = request.args.get('date_to')
    
    query = FeePayment.query.join(Student)
    
    if date_from:
        query = query.filter(FeePayment.payment_date >= datetime.fromisoformat(date_from).date())
    
    if date_to:
        query = query.filter(FeePayment.payment_date <= datetime.fromisoformat(date_to).date())
    
    payments = query.order_by(FeePayment.payment_date.desc()).all()
    
    # Create CSV
    output = io.StringIO()
    writer = csv.writer(output)
    
    writer.writerow([
        'Receipt Number', 'Date', 'Student ID', 'Student Name',
        'Course', 'Amount', 'Payment Mode', 'Transaction ID', 'Remarks'
    ])
    
    for payment in payments:
        writer.writerow([
            payment.receipt_number,
            payment.payment_date.isoformat(),
            payment.student.student_id,
            f"{payment.student.first_name} {payment.student.last_name}",
            payment.student.course,
            payment.amount,
            payment.payment_mode,
            payment.transaction_id,
            payment.remarks
        ])
    
    output.seek(0)
    return send_file(
        io.BytesIO(output.getvalue().encode('utf-8')),
        mimetype='text/csv',
        as_attachment=True,
        download_name=f'fee_payments_{datetime.now().strftime("%Y%m%d")}.csv'
    )

@reports_bp.route('/export/notes', methods=['GET'])
@login_required
@role_required('admin', 'librarian')
def export_notes():
    """Export notes list to CSV"""
    notes = Note.query.order_by(Note.uploaded_at.desc()).all()
    
    # Create CSV
    output = io.StringIO()
    writer = csv.writer(output)
    
    writer.writerow([
        'Title', 'Category', 'File Type', 'Uploaded By', 'Upload Date',
        'Views', 'Downloads', 'Visibility', 'Tags'
    ])
    
    for note in notes:
        writer.writerow([
            note.title,
            note.category,
            note.file_type,
            note.uploader.full_name if note.uploader else 'Unknown',
            note.uploaded_at.isoformat() if note.uploaded_at else '',
            note.views,
            note.downloads,
            note.visibility,
            note.tags
        ])
    
    output.seek(0)
    return send_file(
        io.BytesIO(output.getvalue().encode('utf-8')),
        mimetype='text/csv',
        as_attachment=True,
        download_name=f'notes_{datetime.now().strftime("%Y%m%d")}.csv'
    )

@reports_bp.route('/analytics/notes', methods=['GET'])
@login_required
@role_required('admin', 'librarian')
def notes_analytics():
    """Get notes analytics"""
    # Upload trend (last 30 days)
    thirty_days_ago = datetime.now() - datetime.timedelta(days=30)
    daily_uploads = db.session.query(
        func.date(Note.uploaded_at),
        func.count(Note.id)
    ).filter(
        Note.uploaded_at >= thirty_days_ago
    ).group_by(func.date(Note.uploaded_at)).all()
    
    # Most viewed notes
    top_viewed = Note.query.order_by(Note.views.desc()).limit(10).all()
    
    # Most downloaded notes
    top_downloaded = Note.query.order_by(Note.downloads.desc()).limit(10).all()
    
    # Category distribution
    categories = db.session.query(
        Note.category,
        func.count(Note.id),
        func.sum(Note.views),
        func.sum(Note.downloads)
    ).group_by(Note.category).all()
    
    return jsonify({
        'daily_uploads': [{
            'date': date.isoformat() if date else None,
            'count': count
        } for date, count in daily_uploads],
        'top_viewed': [{
            'id': n.id,
            'title': n.title,
            'views': n.views,
            'category': n.category
        } for n in top_viewed],
        'top_downloaded': [{
            'id': n.id,
            'title': n.title,
            'downloads': n.downloads,
            'category': n.category
        } for n in top_downloaded],
        'categories': [{
            'name': cat,
            'count': count,
            'views': views or 0,
            'downloads': downloads or 0
        } for cat, count, views, downloads in categories]
    }), 200

@reports_bp.route('/analytics/students', methods=['GET'])
@login_required
@role_required('admin', 'librarian')
def students_analytics():
    """Get students analytics"""
    # Total students
    total_students = Student.query.filter_by(is_active=True).count()
    
    # Course distribution
    courses = db.session.query(
        Student.course,
        func.count(Student.id)
    ).filter_by(is_active=True).group_by(Student.course).all()
    
    # Batch distribution
    batches = db.session.query(
        Student.batch,
        func.count(Student.id)
    ).filter_by(is_active=True).group_by(Student.batch).all()
    
    # Gender distribution
    genders = db.session.query(
        Student.gender,
        func.count(Student.id)
    ).filter_by(is_active=True).group_by(Student.gender).all()
    
    # Enrollment trend (last 12 months)
    twelve_months_ago = datetime.now() - datetime.timedelta(days=365)
    monthly_enrollments = db.session.query(
        func.strftime('%Y-%m', Student.enrollment_date),
        func.count(Student.id)
    ).filter(
        Student.enrollment_date >= twelve_months_ago.date()
    ).group_by(func.strftime('%Y-%m', Student.enrollment_date)).all()
    
    return jsonify({
        'total_students': total_students,
        'courses': [{'name': course, 'count': count} for course, count in courses if course],
        'batches': [{'name': batch, 'count': count} for batch, count in batches if batch],
        'genders': [{'name': gender, 'count': count} for gender, count in genders if gender],
        'monthly_enrollments': [{
            'month': month,
            'count': count
        } for month, count in monthly_enrollments]
    }), 200

@reports_bp.route('/analytics/fees', methods=['GET'])
@login_required
@role_required('admin', 'librarian')
def fees_analytics():
    """Get fees collection analytics"""
    # Total collection
    total_collected = db.session.query(func.sum(FeePayment.amount)).scalar() or 0
    
    # Monthly collection (last 12 months)
    twelve_months_ago = datetime.now() - datetime.timedelta(days=365)
    monthly_collection = db.session.query(
        func.strftime('%Y-%m', FeePayment.payment_date),
        func.sum(FeePayment.amount)
    ).filter(
        FeePayment.payment_date >= twelve_months_ago.date()
    ).group_by(func.strftime('%Y-%m', FeePayment.payment_date)).all()
    
    # Payment mode distribution
    payment_modes = db.session.query(
        FeePayment.payment_mode,
        func.count(FeePayment.id),
        func.sum(FeePayment.amount)
    ).group_by(FeePayment.payment_mode).all()
    
    # Top paying students
    top_payers = db.session.query(
        Student,
        func.sum(FeePayment.amount).label('total_paid')
    ).join(FeePayment).group_by(Student.id).order_by(
        func.sum(FeePayment.amount).desc()
    ).limit(10).all()
    
    return jsonify({
        'total_collected': float(total_collected),
        'monthly_collection': [{
            'month': month,
            'amount': float(amount)
        } for month, amount in monthly_collection],
        'payment_modes': [{
            'mode': mode,
            'count': count,
            'amount': float(amount)
        } for mode, count, amount in payment_modes],
        'top_payers': [{
            'student_id': student.student_id,
            'student_name': f"{student.first_name} {student.last_name}",
            'total_paid': float(total_paid)
        } for student, total_paid in top_payers]
    }), 200
