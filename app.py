import os
import sqlite3
import io
import json
from datetime import datetime
from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, session, jsonify, send_file, flash
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

from text_engine import TOOL_CATEGORIES, TOOL_INFO, process_tool, metrics

APP_NAME = os.getenv('APP_NAME', 'TextForge Studio')
DB_PATH = os.getenv('DATABASE_PATH', os.path.join(os.path.dirname(__file__), 'instance', 'textforge.db'))
UPLOAD_EXTENSIONS = {'.txt', '.md', '.docx', '.pdf'}

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'change-this-secret-key-before-production')
app.config['MAX_CONTENT_LENGTH'] = 12 * 1024 * 1024


def get_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_db() as db:
        db.executescript('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            tool_id TEXT NOT NULL,
            input_text TEXT NOT NULL,
            output_text TEXT NOT NULL,
            stats_json TEXT NOT NULL,
            created_at TEXT NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(id)
        );
        CREATE TABLE IF NOT EXISTS settings (
            user_id INTEGER PRIMARY KEY,
            default_tone TEXT DEFAULT 'professional',
            default_strength TEXT DEFAULT 'strong',
            brand_name TEXT DEFAULT 'TextForge Studio',
            FOREIGN KEY(user_id) REFERENCES users(id)
        );
        ''')


@app.before_request
def ensure_db():
    init_db()


def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return view(*args, **kwargs)
    return wrapped


def current_user():
    if 'user_id' not in session:
        return None
    with get_db() as db:
        return db.execute('SELECT * FROM users WHERE id=?', (session['user_id'],)).fetchone()


@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    feature_count = sum(len(v) for v in TOOL_CATEGORIES.values())
    return render_template('index.html', app_name=APP_NAME, feature_count=feature_count, categories=TOOL_CATEGORIES)


@app.route('/signup', methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        name = request.form.get('name','').strip()
        email = request.form.get('email','').strip().lower()
        password = request.form.get('password','')
        if not name or not email or len(password) < 6:
            flash('Please enter your name, email, and a password with at least 6 characters.', 'error')
            return render_template('auth.html', mode='signup', app_name=APP_NAME)
        try:
            with get_db() as db:
                cur = db.execute('INSERT INTO users(name,email,password_hash,created_at) VALUES(?,?,?,?)',
                    (name, email, generate_password_hash(password), datetime.utcnow().isoformat()))
                user_id = cur.lastrowid
                db.execute('INSERT INTO settings(user_id) VALUES(?)', (user_id,))
            session['user_id'] = user_id
            return redirect(url_for('dashboard'))
        except sqlite3.IntegrityError:
            flash('This email already has an account. Please login instead.', 'error')
    return render_template('auth.html', mode='signup', app_name=APP_NAME)


@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email','').strip().lower()
        password = request.form.get('password','')
        with get_db() as db:
            user = db.execute('SELECT * FROM users WHERE email=?', (email,)).fetchone()
        if user and check_password_hash(user['password_hash'], password):
            session['user_id'] = user['id']
            return redirect(url_for('dashboard'))
        flash('Invalid email or password.', 'error')
    return render_template('auth.html', mode='login', app_name=APP_NAME)


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


@app.route('/dashboard')
@login_required
def dashboard():
    user = current_user()
    with get_db() as db:
        settings = db.execute('SELECT * FROM settings WHERE user_id=?', (session['user_id'],)).fetchone()
        history = db.execute('SELECT * FROM history WHERE user_id=? ORDER BY id DESC LIMIT 12', (session['user_id'],)).fetchall()
    tools = {cat: [{'id': tid, 'name': TOOL_INFO[tid][0], 'description': TOOL_INFO[tid][1]} for tid in ids] for cat, ids in TOOL_CATEGORIES.items()}
    first_tool = TOOL_CATEGORIES['Smart Writing'][0]
    return render_template('dashboard.html', app_name=APP_NAME, user=user, tools=tools, tool_info=TOOL_INFO, first_tool=first_tool, history=history, settings=settings)


@app.post('/api/process')
@login_required
def api_process():
    data = request.get_json(force=True, silent=True) or {}
    tool_id = data.get('tool_id', 'humanizer')
    text = data.get('text', '')
    params = data.get('params', {}) or {}
    output = process_tool(tool_id, text, params)
    stats = metrics(text, output)
    if data.get('save', True):
        with get_db() as db:
            db.execute('INSERT INTO history(user_id,tool_id,input_text,output_text,stats_json,created_at) VALUES(?,?,?,?,?,?)',
                (session['user_id'], tool_id, text[:10000], output[:15000], json.dumps(stats), datetime.utcnow().isoformat()))
    return jsonify({'ok': True, 'output': output, 'stats': stats, 'tool': TOOL_INFO.get(tool_id, [tool_id])[0]})


@app.post('/api/upload')
@login_required
def api_upload():
    file = request.files.get('file')
    if not file:
        return jsonify({'ok': False, 'error': 'No file uploaded.'}), 400
    filename = secure_filename(file.filename or 'upload.txt')
    ext = os.path.splitext(filename)[1].lower()
    if ext not in UPLOAD_EXTENSIONS:
        return jsonify({'ok': False, 'error': 'Supported files: TXT, MD, DOCX, PDF.'}), 400
    raw = file.read()
    try:
        text = extract_text_from_upload(raw, ext)
        return jsonify({'ok': True, 'filename': filename, 'text': text})
    except Exception as exc:
        return jsonify({'ok': False, 'error': f'Could not read file: {exc}'}), 500


def extract_text_from_upload(raw, ext):
    if ext in ('.txt', '.md'):
        try:
            return raw.decode('utf-8')
        except UnicodeDecodeError:
            return raw.decode('latin-1', errors='ignore')
    if ext == '.docx':
        from docx import Document
        doc = Document(io.BytesIO(raw))
        return '\n'.join(p.text for p in doc.paragraphs if p.text.strip())
    if ext == '.pdf':
        from pypdf import PdfReader
        reader = PdfReader(io.BytesIO(raw))
        pages = []
        for page in reader.pages:
            pages.append(page.extract_text() or '')
        return '\n\n'.join(pages).strip()
    return ''


@app.post('/api/export')
@login_required
def api_export():
    data = request.get_json(force=True, silent=True) or {}
    text = data.get('text','')
    fmt = data.get('format','txt').lower()
    title = data.get('title','TextForge Output')
    safe_title = ''.join(c for c in title if c.isalnum() or c in (' ','_','-')).strip()[:40] or 'textforge-output'
    if fmt == 'txt':
        bio = io.BytesIO(text.encode('utf-8'))
        return send_file(bio, as_attachment=True, download_name=f'{safe_title}.txt', mimetype='text/plain')
    if fmt == 'md':
        bio = io.BytesIO(text.encode('utf-8'))
        return send_file(bio, as_attachment=True, download_name=f'{safe_title}.md', mimetype='text/markdown')
    if fmt == 'docx':
        from docx import Document
        doc = Document()
        doc.add_heading(title, 0)
        for para in text.split('\n'):
            if para.strip().startswith('# '):
                doc.add_heading(para.strip('# ').strip(), level=1)
            elif para.strip().startswith('## '):
                doc.add_heading(para.strip('# ').strip(), level=2)
            elif para.strip().startswith('- '):
                doc.add_paragraph(para.strip()[2:], style='List Bullet')
            else:
                doc.add_paragraph(para)
        bio = io.BytesIO()
        doc.save(bio)
        bio.seek(0)
        return send_file(bio, as_attachment=True, download_name=f'{safe_title}.docx', mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
    if fmt == 'pdf':
        from reportlab.lib.pagesizes import A4
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
        from reportlab.lib.styles import getSampleStyleSheet
        from reportlab.lib.units import inch
        bio = io.BytesIO()
        doc = SimpleDocTemplate(bio, pagesize=A4, rightMargin=0.6*inch, leftMargin=0.6*inch, topMargin=0.6*inch, bottomMargin=0.6*inch)
        styles = getSampleStyleSheet()
        story = [Paragraph(title, styles['Title']), Spacer(1, 12)]
        escaped = (text.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;'))
        for para in escaped.split('\n'):
            story.append(Paragraph(para if para.strip() else ' ', styles['BodyText']))
            story.append(Spacer(1, 6))
        doc.build(story)
        bio.seek(0)
        return send_file(bio, as_attachment=True, download_name=f'{safe_title}.pdf', mimetype='application/pdf')
    return jsonify({'ok': False, 'error': 'Unsupported export format.'}), 400


@app.get('/api/history/<int:item_id>')
@login_required
def api_history_item(item_id):
    with get_db() as db:
        item = db.execute('SELECT * FROM history WHERE id=? AND user_id=?', (item_id, session['user_id'])).fetchone()
    if not item:
        return jsonify({'ok': False, 'error': 'Not found'}), 404
    return jsonify({'ok': True, 'item': dict(item)})


@app.post('/api/settings')
@login_required
def api_settings():
    data = request.get_json(force=True, silent=True) or {}
    tone = data.get('default_tone','professional')
    strength = data.get('default_strength','strong')
    brand = data.get('brand_name', APP_NAME)[:60]
    with get_db() as db:
        db.execute('UPDATE settings SET default_tone=?, default_strength=?, brand_name=? WHERE user_id=?',
                   (tone, strength, brand, session['user_id']))
    return jsonify({'ok': True})


@app.post('/api/clear-history')
@login_required
def api_clear_history():
    with get_db() as db:
        db.execute('DELETE FROM history WHERE user_id=?', (session['user_id'],))
    return jsonify({'ok': True})


if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5000)), debug=os.getenv('FLASK_DEBUG','1') == '1')
