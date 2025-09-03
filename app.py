import os
from flask import Flask, render_template, request, redirect, url_for, flash, abort
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

# ===== Application Configuration =====
app = Flask(__name__)
app.config['SECRET_KEY'] = 'a-very-secret-key-that-should-be-changed'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = "You must log in to access this page."

# ===== Database Models =====
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(50), nullable=False, default='user') # 'admin' or 'user'
    projects = db.relationship('Project', backref='owner', lazy=True)
    notes = db.relationship('Note', backref='owner', lazy=True)

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500))
    image_url = db.Column(db.String(500), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(1000), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ===== Role Decorator =====
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'admin':
            abort(403) # Forbidden
        return f(*args, **kwargs)
    return decorated_function

# ===== Authentication Routes =====
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for('dashboard'))
        flash('Invalid username or password.')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# ===== Main Application Routes =====
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
@login_required
def dashboard():
    if current_user.role == 'admin':
        projects = Project.query.all()
        users = User.query.all()
    else:
        projects = Project.query.filter_by(user_id=current_user.id).all()
        users = [current_user]
    return render_template('dashboard.html', projects=projects, users=users)

# --- IDOR Vulnerabilities Start Here ---

@app.route('/profile/<int:user_id>')
@login_required
def profile(user_id):
    # VULNERABLE: No ownership check.
    user = User.query.get_or_404(user_id)
    return render_template('profile.html', user=user)

@app.route('/project/<int:project_id>')
@login_required
def project_detail(project_id):
    # VULNERABLE: No ownership check.
    project = Project.query.get_or_404(project_id)
    return render_template('project_detail.html', project=project)

@app.route('/project/edit/<int:project_id>', methods=['GET', 'POST'])
@login_required
def edit_project(project_id):
    # VULNERABLE: No ownership check on GET or POST.
    project = Project.query.get_or_404(project_id)
    if request.method == 'POST':
        project.name = request.form.get('name')
        project.description = request.form.get('description')
        project.image_url = request.form.get('image_url')
        db.session.commit()
        flash('Project updated successfully!', 'success')
        return redirect(url_for('project_detail', project_id=project.id))
    return render_template('project_edit.html', project=project)

@app.route('/notes/edit/<int:note_id>', methods=['GET', 'POST'])
@login_required
def edit_note(note_id):
    # VULNERABLE: No ownership check.
    note = Note.query.get_or_404(note_id)
    if request.method == 'POST':
        note.content = request.form.get('content', '')
        db.session.commit()
        flash('Note updated successfully!', 'success')
        return redirect(url_for('dashboard'))
    return render_template('note_edit.html', note=note)

# --- IDOR Vulnerabilities End Here ---


# ===== Secure Admin Page (For Comparison) =====
@app.route('/admin')
@login_required
@admin_required
def admin_panel():
    return render_template('admin_panel.html')

@app.errorhandler(403)
def forbidden_page(e):
    return render_template('403.html'), 403

# ===== Database Setup Function =====
def create_initial_data():
    with app.app_context():
        db.drop_all()
        db.create_all()

        hashed_password = generate_password_hash("password123", method='pbkdf2:sha256')
        admin_user = User(id=1, username="admin", password_hash=hashed_password, role="admin")
        attacker_user = User(id=2, username="atacker", password_hash=hashed_password, role="user")
        
        db.session.add_all([admin_user, attacker_user])
        db.session.commit()

        proj_admin1 = Project(name="Admin's Secret Project", description="This is a project only the admin should be able to edit.", user_id=1, image_url="https://placehold.co/600x400/3498db/ffffff?text=Admin's+Project")
        note_admin1 = Note(content="This is a secret note for the admin.", user_id=1)
        
        proj_attacker1 = Project(name="Attacker's Plan", description="A project belonging to the attacker.", user_id=2)
        note_attacker1 = Note(content="A note for the attacker.", user_id=2)

        db.session.add_all([proj_admin1, note_admin1, proj_attacker1, note_attacker1])
        db.session.commit()
        
        print("Database created with 'admin' (id=1) and 'atacker' (id=2).")

if __name__ == '__main__':
    db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'instance/db.sqlite3')
    if not os.path.exists(db_path):
        create_initial_data()
    app.run(host='0.0.0.0', port=5000, debug=False)