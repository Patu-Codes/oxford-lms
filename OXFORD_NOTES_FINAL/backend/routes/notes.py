"""
Notes management routes — Oxford LMS
View vs Download are two separate, explicitly controlled permissions.
All file serving is authenticated and authorized server-side.
"""
from flask import Blueprint, request, jsonify, session, send_file, Response
from werkzeug.utils import secure_filename
from datetime import datetime
from pathlib import Path
import os
import mimetypes

from models import db, Note, User, Student, Favorite, ActivityLog
from routes.auth import login_required, role_required
from config import Config

notes_bp = Blueprint('notes', __name__)

ALLOWED_EXTENSIONS = {'pdf', 'mp4', 'webm', 'mov', 'ppt', 'pptx'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def get_file_category(ext):
    ext = ext.lower()
    if ext == 'pdf':
        return 'pdf'
    elif ext in ('mp4', 'webm', 'mov'):
        return 'videos'
    elif ext in ('ppt', 'pptx'):
        return 'presentations'
    elif ext in ('doc', 'docx'):
        return 'documents'
    elif ext in ('xls', 'xlsx'):
        return 'spreadsheets'
    elif ext in ('png', 'jpg', 'jpeg', 'gif'):
        return 'images'
    elif ext == 'txt':
        return 'text'
    return 'documents'


def _authorize_note_access(note, user, student=None):
    """
    Returns (allowed: bool, reason: str).
    Enforces visibility AND course/batch access for students.
    Never trusts frontend.
    """
    # Admins always have access
    if user.role == 'admin':
        return True, None

    # Visibility gate
    if note.visibility == 'admin':
        return False, 'Access denied'

    # For students: check course/batch assignment
    if user.role == 'student':
        if student is None:
            student = Student.query.filter_by(user_id=user.id).first()
        if not student:
            return False, 'Student profile not found'

        # If note is scoped to a specific course, student must be in that course
        if note.course_id and student.course_id != note.course_id:
            return False, 'This resource is not available for your course'

        # If note is scoped to a specific batch, student must be in that batch
        if note.batch_id and student.batch_id != note.batch_id:
            return False, 'This resource is not available for your batch'

    return True, None


# ─── LIST / SEARCH ────────────────────────────────────────────────────────────

@notes_bp.route('/', methods=['GET'])
@login_required
def get_notes():
    user_id = session.get('user_id')
    user    = User.query.get(user_id)

    query_str    = request.args.get('query', '')
    category     = request.args.get('category', 'All')
    sort         = request.args.get('sort', 'newest')
    favorites_only = request.args.get('favorites', 'false').lower() == 'true'
    page         = int(request.args.get('page', 1))
    per_page     = int(request.args.get('per_page', 50))

    q = Note.query

    # Visibility filter
    if user.role == 'student':
        q = q.filter(Note.visibility.in_(['all', 'students']))

        # Course/batch scoping — students only see notes for their course/batch
        # (or notes with no course/batch restriction)
        student = Student.query.filter_by(user_id=user_id).first()
        if student:
            q = q.filter(
                db.or_(
                    Note.course_id == None,
                    Note.course_id == student.course_id
                )
            ).filter(
                db.or_(
                    Note.batch_id == None,
                    Note.batch_id == student.batch_id
                )
            )
    elif user.role != 'admin':
        q = q.filter(Note.visibility.in_(['all', 'students']))

    if query_str:
        q = q.filter(db.or_(
            Note.title.ilike(f'%{query_str}%'),
            Note.description.ilike(f'%{query_str}%'),
            Note.tags.ilike(f'%{query_str}%')
        ))
    if category != 'All':
        q = q.filter_by(category=category)
    if favorites_only:
        q = q.join(Favorite).filter(Favorite.user_id == user_id)

    if sort == 'newest':
        q = q.order_by(Note.uploaded_at.desc())
    elif sort == 'oldest':
        q = q.order_by(Note.uploaded_at.asc())
    elif sort == 'title':
        q = q.order_by(Note.title.asc())
    elif sort == 'popular':
        q = q.order_by(Note.views.desc())

    pagination = q.paginate(page=page, per_page=per_page, error_out=False)
    user_faves  = {f.note_id for f in Favorite.query.filter_by(user_id=user_id).all()}

    notes_data = []
    for note in pagination.items:
        d = note.to_dict()          # file_path is NOT in to_dict()
        d['is_favorite'] = note.id in user_faves
        notes_data.append(d)

    return jsonify({
        'notes': notes_data,
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': page,
    }), 200


@notes_bp.route('/<int:note_id>', methods=['GET'])
@login_required
def get_note(note_id):
    note    = Note.query.get_or_404(note_id)
    user_id = session.get('user_id')
    user    = User.query.get(user_id)

    allowed, reason = _authorize_note_access(note, user)
    if not allowed:
        return jsonify({'error': reason}), 403

    is_fave = Favorite.query.filter_by(user_id=user_id, note_id=note_id).first() is not None
    d = note.to_dict()
    d['is_favorite'] = is_fave
    return jsonify({'note': d}), 200


# ─── VIEW (inline, protected) ─────────────────────────────────────────────────

@notes_bp.route('/<int:note_id>/view', methods=['GET'])
@login_required
def view_note(note_id):
    """
    Serve the file for inline viewing only.
    - Students must be authorized (visibility + course/batch).
    - No automatic download — Content-Disposition: inline.
    - Content-Security-Policy prevents embedding in other pages.
    - X-Content-Type-Options prevents MIME sniffing.
    - Cache-Control: no-store prevents disk caching in shared browsers.
    View does NOT require is_downloadable — any accessible note can be viewed.
    """
    note    = Note.query.get_or_404(note_id)
    user_id = session.get('user_id')
    user    = User.query.get(user_id)

    allowed, reason = _authorize_note_access(note, user)
    if not allowed:
        return jsonify({'error': reason}), 403

    file_path = Config.UPLOAD_FOLDER / note.file_path
    if not file_path.exists():
        return jsonify({'error': 'File not found on server'}), 404

    # Increment view counter
    note.views += 1
    db.session.add(ActivityLog(
        user_id=user_id, action='NOTE_VIEWED',
        details=f'Viewed: {note.title}',
        status='SUCCESS', ip_address=request.remote_addr
    ))
    db.session.commit()

    mime, _ = mimetypes.guess_type(str(file_path))
    mime = mime or 'application/octet-stream'

    # Build response with security headers
    response = send_file(
        str(file_path),
        mimetype=mime,
        as_attachment=False,                         # inline — NOT a download
        download_name=f"{note.title}.{note.file_type}"
    )

    # Security headers for protected serving
    response.headers['Content-Disposition'] = f'inline; filename="{note.title}.{note.file_type}"'
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['Cache-Control']          = 'no-store, no-cache, must-revalidate, private'
    response.headers['Pragma']                 = 'no-cache'
    # Allow framing from same origin (our PDF.js canvas viewer) and Google Docs Viewer
    response.headers['X-Frame-Options']        = 'SAMEORIGIN'
    response.headers['Content-Security-Policy'] = (
        "default-src 'self'; "
        "frame-ancestors 'self' https://docs.google.com;"
    )

    return response


# ─── DOWNLOAD (explicit, permission-gated) ────────────────────────────────────

@notes_bp.route('/<int:note_id>/download', methods=['GET'])
@login_required
def download_note(note_id):
    """
    Serve the file as an attachment (download dialog).
    Requires is_downloadable = True for students.
    Admins can always download.
    """
    note    = Note.query.get_or_404(note_id)
    user_id = session.get('user_id')
    user    = User.query.get(user_id)

    # Authorization: visibility + course/batch
    allowed, reason = _authorize_note_access(note, user)
    if not allowed:
        return jsonify({'error': reason}), 403

    # Download permission gate — students only
    if user.role == 'student' and not note.is_downloadable:
        return jsonify({
            'error': 'This note is set to View Only. Downloading is not permitted.'
        }), 403

    file_path = Config.UPLOAD_FOLDER / note.file_path
    if not file_path.exists():
        return jsonify({'error': 'File not found on server'}), 404

    note.downloads += 1
    db.session.add(ActivityLog(
        user_id=user_id, action='NOTE_DOWNLOADED',
        details=f'Downloaded: {note.title}',
        status='SUCCESS', ip_address=request.remote_addr
    ))
    db.session.commit()

    return send_file(
        str(file_path),
        as_attachment=True,
        download_name=f"{note.title}.{note.file_type}"
    )


# ─── UPLOAD ───────────────────────────────────────────────────────────────────

@notes_bp.route('/upload', methods=['POST'])
@login_required
@role_required('admin')
def upload_note():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    file = request.files['file']
    if not file.filename:
        return jsonify({'error': 'No file selected'}), 400
    if not allowed_file(file.filename):
        return jsonify({'error': 'File type not allowed'}), 400

    title       = request.form.get('title', '').strip()
    description = request.form.get('description', '').strip()
    category    = request.form.get('category', 'General')
    visibility  = request.form.get('visibility', 'all')
    tags        = request.form.get('tags', '')

    # Default is View Only — admin must explicitly enable download
    raw_dl      = request.form.get('is_downloadable', 'false').strip().lower()
    is_downloadable = raw_dl in ('true', '1', 'yes', 'on')

    course_id_raw = request.form.get('course_id', '').strip()
    course_id     = int(course_id_raw) if course_id_raw.isdigit() else None
    batch_id_raw  = request.form.get('batch_id', '').strip()
    batch_id      = int(batch_id_raw) if batch_id_raw.isdigit() else None

    if not title:
        return jsonify({'error': 'Title is required'}), 400

    filename      = secure_filename(file.filename)
    file_ext      = filename.rsplit('.', 1)[1].lower()
    file_category = get_file_category(file_ext)

    timestamp       = datetime.now().strftime('%Y%m%d_%H%M%S')
    unique_filename = f"{timestamp}_{filename}"

    upload_dir = Config.UPLOAD_FOLDER / file_category
    upload_dir.mkdir(parents=True, exist_ok=True)
    file_path = upload_dir / unique_filename
    file.save(str(file_path))
    file_size = os.path.getsize(file_path)

    note = Note(
        title=title, description=description, category=category,
        file_path=str(file_path.relative_to(Config.UPLOAD_FOLDER)),
        file_type=file_ext, file_size=file_size,
        uploaded_by=session['user_id'],
        visibility=visibility, tags=tags,
        is_downloadable=is_downloadable,
        course_id=course_id, batch_id=batch_id
    )
    db.session.add(note)
    db.session.add(ActivityLog(
        user_id=session['user_id'], action='NOTE_UPLOADED',
        details=f'Uploaded: {title} | Access: {"View+Download" if is_downloadable else "View Only"}',
        status='SUCCESS', ip_address=request.remote_addr
    ))
    db.session.commit()
    return jsonify({'message': 'Note uploaded', 'note': note.to_dict()}), 201


# ─── UPDATE ───────────────────────────────────────────────────────────────────

@notes_bp.route('/<int:note_id>', methods=['PUT'])
@login_required
@role_required('admin')
def update_note(note_id):
    note = Note.query.get_or_404(note_id)
    data = request.get_json()

    if 'title'           in data: note.title           = data['title'].strip()
    if 'description'     in data: note.description     = data['description'].strip()
    if 'category'        in data: note.category        = data['category']
    if 'visibility'      in data: note.visibility      = data['visibility']
    if 'tags'            in data: note.tags            = data['tags']
    if 'is_downloadable' in data: note.is_downloadable = bool(data['is_downloadable'])
    if 'course_id'       in data: note.course_id       = data['course_id'] or None
    if 'batch_id'        in data: note.batch_id        = data['batch_id'] or None

    db.session.add(ActivityLog(
        user_id=session['user_id'], action='NOTE_UPDATED',
        details=f'Updated: {note.title} | Access: {"View+Download" if note.is_downloadable else "View Only"}',
        status='SUCCESS', ip_address=request.remote_addr
    ))
    db.session.commit()
    return jsonify({'message': 'Note updated', 'note': note.to_dict()}), 200


# ─── DELETE ───────────────────────────────────────────────────────────────────

@notes_bp.route('/<int:note_id>', methods=['DELETE'])
@login_required
@role_required('admin')
def delete_note(note_id):
    note = Note.query.get_or_404(note_id)
    file_path = Config.UPLOAD_FOLDER / note.file_path
    if file_path.exists():
        file_path.unlink()
    title = note.title
    db.session.delete(note)
    db.session.add(ActivityLog(
        user_id=session['user_id'], action='NOTE_DELETED',
        details=f'Deleted: {title}', status='SUCCESS',
        ip_address=request.remote_addr
    ))
    db.session.commit()
    return jsonify({'message': 'Note deleted'}), 200


# ─── FAVORITES ────────────────────────────────────────────────────────────────

@notes_bp.route('/<int:note_id>/favorite', methods=['POST'])
@login_required
def toggle_favorite(note_id):
    Note.query.get_or_404(note_id)
    user_id = session.get('user_id')
    fave    = Favorite.query.filter_by(user_id=user_id, note_id=note_id).first()
    if fave:
        db.session.delete(fave)
        db.session.commit()
        return jsonify({'message': 'Removed from favorites', 'is_favorite': False}), 200
    db.session.add(Favorite(user_id=user_id, note_id=note_id))
    db.session.commit()
    return jsonify({'message': 'Added to favorites', 'is_favorite': True}), 200


# ─── STATS ────────────────────────────────────────────────────────────────────

@notes_bp.route('/stats', methods=['GET'])
@login_required
def get_note_stats():
    user = User.query.get(session['user_id'])
    q    = Note.query if user.role == 'admin' else Note.query.filter(Note.visibility.in_(['all', 'students']))
    return jsonify({
        'total_notes':     q.count(),
        'total_views':     db.session.query(db.func.sum(Note.views)).scalar() or 0,
        'total_downloads': db.session.query(db.func.sum(Note.downloads)).scalar() or 0,
    }), 200
