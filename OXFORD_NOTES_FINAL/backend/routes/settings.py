"""
Institute settings routes
"""
from flask import Blueprint, request, jsonify, session
from models import db, InstituteSetting, ActivityLog
from routes.auth import login_required, role_required

settings_bp = Blueprint('settings', __name__)


@settings_bp.route('/', methods=['GET'])
@login_required
def get_settings():
    settings = InstituteSetting.query.first()
    if not settings:
        settings = InstituteSetting()
        db.session.add(settings)
        db.session.commit()
    return jsonify({'settings': settings.to_dict()}), 200


@settings_bp.route('/', methods=['PUT'])
@login_required
@role_required('admin')
def update_settings():
    data = request.get_json()
    settings = InstituteSetting.query.first()
    if not settings:
        settings = InstituteSetting()
        db.session.add(settings)

    fields = [
        'institute_name', 'institute_address', 'institute_phone',
        'institute_email', 'institute_website', 'receipt_prefix',
        'receipt_footer', 'authorized_signatory', 'currency_symbol'
    ]
    for field in fields:
        if field in data:
            setattr(settings, field, data[field])

    db.session.add(ActivityLog(
        user_id=session['user_id'], action='SETTINGS_UPDATED',
        details='Institute settings updated', status='SUCCESS',
        ip_address=request.remote_addr
    ))
    db.session.commit()
    return jsonify({'message': 'Settings updated', 'settings': settings.to_dict()}), 200
