"""
Authentication routes
"""
from flask import Blueprint, request, jsonify, session
from datetime import datetime
from models import db, User, ActivityLog
from functools import wraps

auth_bp = Blueprint('auth', __name__)

def login_required(f):
    """Decorator to require login"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'error': 'Authentication required'}), 401
        return f(*args, **kwargs)
    return decorated_function

def role_required(*roles):
    """Decorator to require specific roles"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_id' not in session:
                return jsonify({'error': 'Authentication required'}), 401
            
            user = User.query.get(session['user_id'])
            if not user or user.role not in roles:
                return jsonify({'error': 'Permission denied'}), 403
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

@auth_bp.route('/login', methods=['POST'])
def login():
    """User login endpoint"""
    data = request.get_json()
    username = data.get('username', '').strip()
    password = data.get('password', '')
    
    if not username or not password:
        return jsonify({'error': 'Username and password required'}), 400
    
    user = User.query.filter_by(username=username).first()
    
    if not user or not user.check_password(password):
        # Log failed attempt
        log = ActivityLog(
            user_id=user.id if user else None,
            action='LOGIN_FAILED',
            details=f'Failed login attempt for username: {username}',
            status='FAILED',
            ip_address=request.remote_addr
        )
        db.session.add(log)
        db.session.commit()
        return jsonify({'error': 'Invalid username or password'}), 401
    
    if not user.is_active:
        return jsonify({'error': 'Account is inactive'}), 403
    
    # Update last login
    user.last_login = datetime.utcnow()
    
    # Log successful login
    log = ActivityLog(
        user_id=user.id,
        action='LOGIN',
        details=f'User {username} logged in successfully',
        status='SUCCESS',
        ip_address=request.remote_addr
    )
    db.session.add(log)
    db.session.commit()
    
    # Set session
    session['user_id'] = user.id
    session['username'] = user.username
    session['role'] = user.role
    session.permanent = True
    
    return jsonify({
        'message': 'Login successful',
        'user': user.to_dict()
    }), 200

@auth_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    """User logout endpoint"""
    user_id = session.get('user_id')
    username = session.get('username')
    
    # Log logout
    if user_id:
        log = ActivityLog(
            user_id=user_id,
            action='LOGOUT',
            details=f'User {username} logged out',
            status='SUCCESS',
            ip_address=request.remote_addr
        )
        db.session.add(log)
        db.session.commit()
    
    session.clear()
    return jsonify({'message': 'Logout successful'}), 200

@auth_bp.route('/me', methods=['GET'])
@login_required
def get_current_user():
    """Get current logged-in user"""
    user = User.query.get(session['user_id'])
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify({'user': user.to_dict()}), 200

@auth_bp.route('/change-password', methods=['POST'])
@login_required
def change_password():
    """Change user password"""
    data = request.get_json()
    old_password = data.get('old_password')
    new_password = data.get('new_password')
    
    if not old_password or not new_password:
        return jsonify({'error': 'Old and new passwords required'}), 400
    
    if len(new_password) < 6:
        return jsonify({'error': 'Password must be at least 6 characters'}), 400
    
    user = User.query.get(session['user_id'])
    
    if not user.check_password(old_password):
        return jsonify({'error': 'Current password is incorrect'}), 400
    
    user.set_password(new_password)
    
    # Log password change
    log = ActivityLog(
        user_id=user.id,
        action='PASSWORD_CHANGED',
        details='User changed their password',
        status='SUCCESS',
        ip_address=request.remote_addr
    )
    db.session.add(log)
    db.session.commit()
    
    return jsonify({'message': 'Password changed successfully'}), 200

@auth_bp.route('/check-session', methods=['GET'])
def check_session():
    """Check if user has active session"""
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
        if user and user.is_active:
            return jsonify({
                'authenticated': True,
                'user': user.to_dict()
            }), 200
    
    return jsonify({'authenticated': False}), 200
