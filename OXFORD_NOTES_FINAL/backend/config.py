"""
Configuration for Oxford LMS - MongoDB Version
"""
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# BASE_DIR is backend/
BASE_DIR = Path(__file__).resolve().parent
# PROJECT_ROOT is the parent directory containing frontend/ and backend/
PROJECT_ROOT = BASE_DIR.parent


class Config:
    # Security
    SECRET_KEY = os.environ.get('SECRET_KEY', 'oxford-lms-change-in-production-please')

    # MongoDB Configuration
    MONGODB_URI = os.environ.get('MONGODB_URI')
    DB_NAME = os.environ.get('DB_NAME', 'oxford_lms')

    # File uploads (in backend/)
    UPLOAD_FOLDER    = BASE_DIR / 'uploads'
    EXPORT_FOLDER    = BASE_DIR / 'exports'
    BACKUP_FOLDER    = BASE_DIR / 'backups'
    MAX_CONTENT_LENGTH = 50 * 1024 * 1024  # default, overridden below after dirs created

    ALLOWED_EXTENSIONS = {
        'pdf', 'doc', 'docx', 'ppt', 'pptx', 'xls', 'xlsx',
        'txt', 'png', 'jpg', 'jpeg', 'gif', 'zip', 'mp4', 'webm', 'mov'
    }

    # Sessions
    PERMANENT_SESSION_LIFETIME = 86400  # 24 hours

    # Branding
    APP_NAME    = 'OXFORD LMS'
    APP_VERSION = '4.0'

    # Create required directories
    for _folder in [UPLOAD_FOLDER, EXPORT_FOLDER, BACKUP_FOLDER]:
        _folder.mkdir(parents=True, exist_ok=True)
    for _sub in ['pdf', 'documents', 'presentations', 'spreadsheets',
                 'images', 'text', 'assignments', 'certificates',
                 'images/profiles', 'videos']:
        (UPLOAD_FOLDER / _sub).mkdir(parents=True, exist_ok=True)

    # Video files can be large — allow up to 500 MB
    MAX_CONTENT_LENGTH = int(os.environ.get('MAX_UPLOAD_MB', 500)) * 1024 * 1024


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False
    # Enforce env vars in production
    SECRET_KEY = os.environ.get('SECRET_KEY') or Config.SECRET_KEY
    
    # Validate MongoDB URI in production
    if not Config.MONGODB_URI:
        raise ValueError("MONGODB_URI must be set in production environment")


config_by_name = {
    'development': DevelopmentConfig,
    'production':  ProductionConfig,
    'default':     DevelopmentConfig,
}
