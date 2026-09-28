"""
Fee management routes — Oxford LMS
"""
from flask import Blueprint, request, jsonify, session, send_file
from datetime import datetime
from sqlalchemy import func
import secrets

from models import db, FeePayment, FeeAccount, Student, StudentFeeAccount, User, ActivityLog, InstituteSetting, Course
from routes.auth import login_required, role_required
from utils.pdf_generator import generate_fee_receipt

fees_bp = Blueprint('fees', __name__)


def _next_receipt_number():
    settings = InstituteSetting.query.first()
    prefix = settings.receipt_prefix if settings else 'OXLMS'
    year   = datetime.now().strftime('%Y')
    # Find highest existing receipt for this prefix+year
    like   = f"{prefix}/{year}/%"
    last   = FeePayment.query.filter(
        FeePayment.receipt_number.like(like)
    ).order_by(FeePayment.receipt_number.desc()).first()
    if last and last.receipt_number:
        try:
            seq = int(last.receipt_number.split('/')[-1]) + 1
        except Exception:
            seq = 1
    else:
        seq = 1
    return f"{prefix}/{year}/{seq:04d}"


# ─── FEE ACCOUNT (course-level) ───────────────────────────────────────────────

@fees_bp.route('/accounts', methods=['GET'])
@login_required
@role_required('admin')
def get_fee_accounts():
    accounts = FeeAccount.query.all()
    return jsonify({'fee_accounts': [
        {'id': a.id, 'course': a.course, 'batch': a.batch,
         'total_fee': a.total_fee, 'description': a.description}
        for a in accounts
    ]}), 200


# ─── STUDENT FEE ACCOUNT ──────────────────────────────────────────────────────

@fees_bp.route('/student-account/<int:student_id>', methods=['GET'])
@login_required
def get_student_fee_account(student_id):
    student = Student.query.get_or_404(student_id)
    user = User.query.get(session['user_id'])
    if user.role == 'student' and student.user_id != session['user_id']:
        return jsonify({'error': 'Access denied'}), 403

    acc = student.fee_account
    total_paid = db.session.query(func.sum(FeePayment.amount)).filter_by(
        student_id=student_id).scalar() or 0
    total_fee  = acc.total_fee if acc else (student.total_fee or 0)
    remaining  = total_fee - float(total_paid)

    return jsonify({
        'student': student.to_dict(),
        'fee_account': acc.to_dict() if acc else None,
        'total_fee':   total_fee,
        'total_paid':  float(total_paid),
        'remaining':   max(remaining, 0),
    }), 200


@fees_bp.route('/student-account/<int:student_id>', methods=['PUT'])
@login_required
@role_required('admin')
def upsert_student_fee_account(student_id):
    student = Student.query.get_or_404(student_id)
    data = request.get_json()
    acc = student.fee_account
    if not acc:
        acc = StudentFeeAccount(student_id=student_id)
        db.session.add(acc)

    if 'total_fee' in data:
        acc.total_fee = float(data['total_fee'])
        student.total_fee = float(data['total_fee'])
    if 'installment_amount' in data:
        acc.installment_amount = float(data['installment_amount']) if data['installment_amount'] else None
    if 'installment_freq' in data:
        acc.installment_freq = data['installment_freq']
    if 'next_due_date' in data and data['next_due_date']:
        acc.next_due_date = datetime.fromisoformat(data['next_due_date']).date()
    if 'remarks' in data:
        acc.remarks = data['remarks']

    db.session.add(ActivityLog(
        user_id=session['user_id'], action='FEE_ACCOUNT_UPDATED',
        details=f'Updated fee account for student {student.student_id}',
        status='SUCCESS', ip_address=request.remote_addr
    ))
    db.session.commit()
    return jsonify({'message': 'Fee account updated', 'fee_account': acc.to_dict()}), 200


# ─── PAYMENTS ─────────────────────────────────────────────────────────────────

@fees_bp.route('/payments', methods=['GET'])
@login_required
def get_payments():
    user_id  = session.get('user_id')
    user     = User.query.get(user_id)
    student_id_filter = request.args.get('student_id', type=int)
    date_from = request.args.get('date_from')
    date_to   = request.args.get('date_to')

    query = FeePayment.query.join(Student)

    if user.role == 'student':
        student = Student.query.filter_by(user_id=user_id).first()
        if not student:
            return jsonify({'payments': []}), 200
        query = query.filter(FeePayment.student_id == student.id)
    elif student_id_filter:
        query = query.filter(FeePayment.student_id == student_id_filter)

    if date_from:
        query = query.filter(FeePayment.payment_date >= datetime.fromisoformat(date_from).date())
    if date_to:
        query = query.filter(FeePayment.payment_date <= datetime.fromisoformat(date_to).date())

    payments = query.order_by(FeePayment.payment_date.desc()).all()
    results  = []
    for p in payments:
        d = p.to_dict()
        d['student_name']   = f"{p.student.first_name} {p.student.last_name}"
        d['student_number'] = p.student.student_id
        results.append(d)
    return jsonify({'payments': results}), 200


@fees_bp.route('/payments', methods=['POST'])
@login_required
@role_required('admin')
def record_payment():
    data = request.get_json()
    for field in ['student_id', 'amount', 'payment_mode']:
        if not data.get(field):
            return jsonify({'error': f'{field} is required'}), 400

    amount = float(data['amount'])
    if amount <= 0:
        return jsonify({'error': 'Amount must be greater than 0'}), 400

    student = Student.query.get(int(data['student_id']))
    if not student:
        return jsonify({'error': 'Student not found'}), 404

    # Safety: check remaining balance
    acc = student.fee_account
    total_fee  = acc.total_fee if acc else (student.total_fee or 0)
    total_paid = db.session.query(func.sum(FeePayment.amount)).filter_by(
        student_id=student.id).scalar() or 0
    remaining  = total_fee - float(total_paid)
    if total_fee > 0 and amount > remaining + 0.01:
        return jsonify({'error': f'Payment exceeds remaining balance (Rs. {remaining:.2f})'}), 400

    settings = InstituteSetting.query.first()
    receipt_number = _next_receipt_number()
    payment_date   = datetime.fromisoformat(data['payment_date']).date() if data.get('payment_date') else datetime.now().date()

    payment = FeePayment(
        student_id=student.id,
        course_id=student.course_id,
        batch_id=student.batch_id,
        amount=amount,
        payment_date=payment_date,
        payment_mode=data['payment_mode'],
        transaction_id=data.get('transaction_id', ''),
        receipt_number=receipt_number,
        remarks=data.get('remarks', ''),
        collected_by=session['user_id'],
        institute_name=settings.institute_name if settings else 'Oxford LMS'
    )
    db.session.add(payment)
    db.session.add(ActivityLog(
        user_id=session['user_id'], action='PAYMENT_RECORDED',
        details=f'Payment of Rs.{amount} recorded for {student.first_name} {student.last_name} | Receipt: {receipt_number}',
        status='SUCCESS', ip_address=request.remote_addr
    ))
    db.session.commit()
    return jsonify({
        'message': 'Payment recorded',
        'payment': {**payment.to_dict(), 'student_name': f"{student.first_name} {student.last_name}"}
    }), 201


@fees_bp.route('/payments/<int:payment_id>', methods=['DELETE'])
@login_required
@role_required('admin')
def delete_payment(payment_id):
    payment = FeePayment.query.get_or_404(payment_id)
    receipt = payment.receipt_number
    db.session.delete(payment)
    db.session.add(ActivityLog(
        user_id=session['user_id'], action='PAYMENT_DELETED',
        details=f'Deleted payment {receipt}', status='SUCCESS',
        ip_address=request.remote_addr
    ))
    db.session.commit()
    return jsonify({'message': 'Payment deleted'}), 200


@fees_bp.route('/payments/<int:payment_id>/receipt', methods=['GET'])
@login_required
def get_receipt(payment_id):
    payment = FeePayment.query.get_or_404(payment_id)
    user = User.query.get(session['user_id'])
    if user.role == 'student':
        student = Student.query.filter_by(user_id=session['user_id']).first()
        if not student or payment.student_id != student.id:
            return jsonify({'error': 'Access denied'}), 403
    pdf_path = generate_fee_receipt(payment)
    return send_file(pdf_path, as_attachment=True,
                     download_name=f'Receipt_{payment.receipt_number.replace("/", "-")}.pdf')


# ─── STUDENT PAYMENT ENDPOINTS ────────────────────────────────────────────────

@fees_bp.route('/student/<int:student_id>/summary', methods=['GET'])
@login_required
def get_fee_summary(student_id):
    student = Student.query.get_or_404(student_id)
    user = User.query.get(session['user_id'])
    if user.role == 'student' and student.user_id != session['user_id']:
        return jsonify({'error': 'Access denied'}), 403

    acc = student.fee_account
    total_fee  = acc.total_fee if acc else (student.total_fee or 0)
    total_paid = db.session.query(func.sum(FeePayment.amount)).filter_by(
        student_id=student_id).scalar() or 0
    payments   = FeePayment.query.filter_by(student_id=student_id).order_by(
        FeePayment.payment_date.desc()).all()

    return jsonify({
        'student': student.to_dict(),
        'fee_account': acc.to_dict() if acc else None,
        'total_fee':   total_fee,
        'total_paid':  float(total_paid),
        'remaining':   max(total_fee - float(total_paid), 0),
        'payments': [{**p.to_dict()} for p in payments]
    }), 200


@fees_bp.route('/student/<int:student_id>/payments', methods=['GET'])
@login_required
def get_student_payments(student_id):
    student = Student.query.get_or_404(student_id)
    user = User.query.get(session['user_id'])
    if user.role == 'student' and student.user_id != session['user_id']:
        return jsonify({'error': 'Access denied'}), 403
    payments = FeePayment.query.filter_by(student_id=student_id).order_by(
        FeePayment.payment_date.desc()).all()
    return jsonify({'payments': [p.to_dict() for p in payments]}), 200


# ─── STATS ────────────────────────────────────────────────────────────────────

@fees_bp.route('/stats', methods=['GET'])
@login_required
@role_required('admin')
def get_fee_stats():
    total = db.session.query(func.sum(FeePayment.amount)).scalar() or 0
    first_of_month = datetime.now().replace(day=1).date()
    month = db.session.query(func.sum(FeePayment.amount)).filter(
        FeePayment.payment_date >= first_of_month).scalar() or 0
    modes = db.session.query(FeePayment.payment_mode, func.sum(FeePayment.amount))\
        .group_by(FeePayment.payment_mode).all()
    return jsonify({
        'total_collected': float(total),
        'month_collected': float(month),
        'payment_modes': [{'mode': m, 'amount': float(a)} for m, a in modes]
    }), 200
