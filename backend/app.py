from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import os
from pathlib import Path
import mimetypes
from mutagen import File as MutagenFile
from dotenv import load_dotenv
import ssl
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from config import Config
from functools import wraps
from flask import redirect, url_for

load_dotenv()
BASE_PATH = os.getenv('BASE_PATH')
FRONTEND_URL = os.getenv('FRONTEND_URL')

app = Flask(__name__)
app.static_folder = 'static'
CORS(app, 
     resources={r"/*": {
        "origins": [FRONTEND_URL, "http://localhost:3000"],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"],
        "supports_credentials": True,
        "expose_headers": ["Set-Cookie"]
     }})

     # הוסף את זה לפני כל ראוט
@app.before_request
def before_request():
    if request.method == "OPTIONS":
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type'
        }
        return ('', 204, headers)


EXTENSION_MAPPING = {
    'jpg': ['jpg', 'jpeg'],
    'mp3': ['mp3', 'MP3'],
    'mp4': ['mp4', 'MP4'],
    'wav': ['wav', 'WAV'],
    'm4a': ['m4a', 'M4A'],
    'avi': ['avi', 'AVI'],
    'mov': ['mov', 'MOV'],
    'pdf': ['pdf', 'PDF'],
    'txt': ['txt', 'TXT'],
    'doc': ['doc', 'docx', 'DOC', 'DOCX'],
    'zip': ['zip', 'ZIP'],
    'rar': ['rar', 'RAR']
}

def is_safe_path(path):
    """בדיקת תקינות הנתיב"""
    try:
        # אם זה נתיב מוחלט (מתחיל ב-C:\ או כדומה)
        if path and path[1:3] == ':\\':
            requested = Path(path).resolve()
        else:
            # אם זה נתיב יחסי, נוסיף אותו לנתיב הבסיס
            requested = Path(os.path.join(BASE_PATH, path)).resolve()
        return requested.exists()
    except:
        return False

def get_file_info(file_path):
    stats = os.stat(file_path)
    file_type = mimetypes.guess_type(file_path)[0]
    
    info = {
        'name': os.path.basename(file_path),
        'size': stats.st_size,
        'type': file_type,
        'duration': None,
        'extension': os.path.splitext(file_path)[1].lower()
    }
    
    if file_type and (file_type.startswith('audio/') or file_type.startswith('video/')):
        try:
            media_info = MutagenFile(file_path)
            if hasattr(media_info, 'info') and hasattr(media_info.info, 'length'):
                info['duration'] = media_info.info.length
        except:
            pass
            
    return info

def normalize_extension(ext):
    """ממפה סיומות קבצים לפורמט אחיד"""
    ext = ext.lower().replace('.', '')
    for main_ext, variations in EXTENSION_MAPPING.items():
        if ext in variations:
            return main_ext
    return ext

def auth_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return jsonify({'error': 'Unauthorized'}), 401
        return f(*args, **kwargs)
    return decorated_function

@app.route('/list-directory', methods=['POST'])
@login_required
def list_directory():
    requested_path = request.json.get('path', '')
    file_types = request.json.get('fileTypes', [])
    
    if requested_path and requested_path[1:3] == ':\\':
        full_path = requested_path
    else:
        full_path = BASE_PATH
    
    if not is_safe_path(full_path):
        return jsonify({'error': f'Invalid path: {full_path}'}), 403
    
    try:
        files = []
        for item in os.listdir(full_path):
            item_path = os.path.join(full_path, item)
            is_directory = os.path.isdir(item_path)
            
            # בדיקת סיומת הקובץ
            extension = os.path.splitext(item)[1].lower().replace('.', '')
            
            # אם זו תיקייה, נוסיף רק אם אין סינון פעיל
            if is_directory:
                if not file_types:  # רק אם אין סינון פעיל
                    files.append({
                        'name': item,
                        'isDirectory': True,
                        'size': 0,
                        'type': None,
                        'extension': None
                    })
                continue

            # אם יש סינון פעיל, נוסיף רק קבצים שמתאימים לסינון
            if not file_types or extension in file_types:
                file_info = {
                    'name': item,
                    'isDirectory': False,
                    'size': os.path.getsize(item_path),
                    'type': mimetypes.guess_type(item_path)[0],
                    'extension': extension,
                    'duration': None
                }
                
                if extension in ['mp3', 'mp4']:
                    try:
                        media_info = MutagenFile(item_path)
                        if hasattr(media_info, 'info') and hasattr(media_info.info, 'length'):
                            file_info['duration'] = media_info.info.length
                    except:
                        pass
                
                files.append(file_info)

        return jsonify({'files': files})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/list-directories', methods=['POST'])
@auth_required
def list_directories():
    requested_path = request.json.get('path', '')
    
    # אם זה נתיב מוחלט, נשתמש בו כמו שהוא
    if requested_path and requested_path[1:3] == ':\\':
        full_path = requested_path
    else:
        # אחרת, נשתמש בנתיב הבסיסי
        full_path = BASE_PATH
    
    if not is_safe_path(full_path):
        return jsonify({'error': f'Invalid path: {full_path}'}), 403
        
    try:
        directories = [d for d in os.listdir(full_path) 
                      if os.path.isdir(os.path.join(full_path, d))]
        return jsonify({'directories': sorted(directories)})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/Browser/', defaults={'path': ''})
@app.route('/Browser/<path:path>')
def serve_browser(path):
    if path and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    return send_from_directory(app.static_folder, 'index.html')

app.config.from_object(Config)

login_manager = LoginManager()
login_manager.init_app(app)

# משתמש פשוט בלי DB
class User(UserMixin):
    def __init__(self, username):
        self.id = username
        self.username = username

@login_manager.user_loader
def load_user(username):
    if username == app.config['ADMIN_USERNAME']:
        return User(username)
    return None

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    if (data['username'] == app.config['ADMIN_USERNAME'] and 
        data['password'] == app.config['ADMIN_PASSWORD']):
        user = User(data['username'])
        login_user(user)
        return jsonify({'success': True})
    return jsonify({'error': 'Invalid credentials'}), 401

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return jsonify({'success': True})

@app.route('/check-auth')
def check_auth():
    if current_user.is_authenticated:
        return jsonify({'authenticated': True})
    return jsonify({'authenticated': False})

if __name__ == '__main__':
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(
        os.getenv('SSL_CERT_PATH'),
        os.getenv('SSL_KEY_PATH')
    )
    app.run(host='0.0.0.0', port=443, ssl_context=context)