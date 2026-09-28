"""
OXFORD LMS - MongoDB Version
Professional Learning Management System for Educational Institutions
"""
import os
from flask import Flask, render_template, request, jsonify, send_file, session, redirect, url_for, send_from_directory
from flask_cors import CORS
from pathlib import Path
import secrets

from config import Config
from database_mongo import init_db, close_db
from routes.auth import auth_bp
from routes.notes import notes_bp
from routes.students import students_bp
from routes.attendance import attendance_bp
from routes.fees import fees_bp
from routes.reports import reports_bp
from routes.dashboard import dashboard_bp
from routes.courses import courses_bp
from routes.batches import batches_bp
from routes.settings import settings_bp

# Get the base directory (backend/)
BASE_DIR = Path(__file__).resolve().parent
# Frontend is one level up, then into frontend/
FRONTEND_DIR = BASE_DIR.parent / 'frontend'


def create_app(config_class=Config):
    app = Flask(__name__, 
                static_folder=str(FRONTEND_DIR / 'static'),
                template_folder=str(FRONTEND_DIR / 'templates'))
    app.config.from_object(config_class)

    CORS(app, supports_credentials=True)

    # Register blueprints
    app.register_blueprint(auth_bp,       url_prefix='/api/auth')
    app.register_blueprint(notes_bp,      url_prefix='/api/notes')
    app.register_blueprint(students_bp,   url_prefix='/api/students')
    app.register_blueprint(attendance_bp, url_prefix='/api/attendance')
    app.register_blueprint(fees_bp,       url_prefix='/api/fees')
    app.register_blueprint(reports_bp,    url_prefix='/api/reports')
    app.register_blueprint(dashboard_bp,  url_prefix='/api/dashboard')
    app.register_blueprint(courses_bp,    url_prefix='/api/courses')
    app.register_blueprint(batches_bp,    url_prefix='/api/batches')
    app.register_blueprint(settings_bp,   url_prefix='/api/settings')

    # Initialize MongoDB
    with app.app_context():
        init_db()

    # Cleanup on app teardown
    @app.teardown_appcontext
    def cleanup(exception=None):
        # MongoDB connection pool is managed automatically
        pass

    # Page routes
    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/login')
    def login_page():
        return render_template('login.html')

    @app.route('/dashboard')
    def dashboard_page():
        return render_template('dashboard.html')

    # /uploads is intentionally NOT exposed publicly.
    # All file serving goes through /api/notes/<id>/view or /api/notes/<id>/download
    # which enforce authentication and per-note permissions.
    # Profile images have their own authenticated endpoint below.

    @app.route('/api/profile-image/<path:filename>')
    def serve_profile_image(filename):
        """Serve profile images — authenticated users only."""
        if 'user_id' not in session:
            return jsonify({'error': 'Authentication required'}), 401
        # Only allow images/profiles/ subdirectory
        safe = filename.replace('\\', '/')
        if not safe.startswith('images/profiles/'):
            return jsonify({'error': 'Forbidden'}), 403
        upload_folder = app.config.get('UPLOAD_FOLDER', Path('uploads'))
        return send_from_directory(str(upload_folder), safe)

    @app.route('/health')
    def health():
        return jsonify({'status': 'healthy', 'app': 'Oxford LMS', 'version': '4.0', 'database': 'MongoDB'})

    return app


app = create_app()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
