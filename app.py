from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'zenith_secret_2026'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///zenith.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ── MODELS ──────────────────────────────────────────────
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    university = db.Column(db.String(100))
    level = db.Column(db.Integer, default=1)
    xp = db.Column(db.Integer, default=0)

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.Text)
    xp = db.Column(db.Integer, default=100)
    world = db.Column(db.String(50))
    author = db.Column(db.String(100))
    progress = db.Column(db.Integer, default=0)
    vacancies = db.Column(db.Integer, default=3)

# ── SEED DATA ────────────────────────────────────────────
projects_database = {
    "tech": [
        {"name": "Neural Interface UI", "lead": "Kavyansh Kulshrestha", "email": "kavyansh@zenith.edu", "vacancies": 3, "progress": 65, "desc": "Building a brain-computer bridge."},
        {"name": "Rural Civic-Sync", "lead": "Nandini Saraswat", "email": "nandini@zenith.edu", "vacancies": 5, "progress": 15, "desc": "Offline governance tool."},
        {"name": "Quantum Cryptography", "lead": "Ishaan Verma", "email": "ishaan@zenith.edu", "vacancies": 2, "progress": 45, "desc": "Next-gen security protocols."},
        {"name": "AI Energy Grid", "lead": "Sara Khan", "email": "sara@zenith.edu", "vacancies": 4, "progress": 30, "desc": "Optimizing renewable energy distribution."}
    ],
    "creative": [
        {"name": "Aether Branding", "lead": "Etiksha Jain", "email": "etiksha@zenith.edu", "vacancies": 2, "progress": 80, "desc": "Digital visual identity."},
        {"name": "Metaverse Gallery", "lead": "Rohan Das", "email": "rohan@zenith.edu", "vacancies": 6, "progress": 20, "desc": "VR art exhibition space."},
        {"name": "Sonic UI", "lead": "Maya Iyer", "email": "maya@zenith.edu", "vacancies": 3, "progress": 55, "desc": "Auditory feedback systems for web interfaces."}
    ],
    "research": [
        {"name": "Quantum Data Viz", "lead": "Dr. Aris", "email": "aris@zenith.edu", "vacancies": 1, "progress": 40, "desc": "Multi-dimensional data sets."},
        {"name": "Bio-Polymer Synthesis", "lead": "Liam Chen", "email": "liam@zenith.edu", "vacancies": 4, "progress": 10, "desc": "Eco-friendly plastic alternatives."},
        {"name": "Fusion Analytics", "lead": "Elena Rossi", "email": "elena@zenith.edu", "vacancies": 2, "progress": 75, "desc": "Plasma stability prediction models."}
    ],
    "economy": [
        {"name": "FinTech Dashboard", "lead": "Rahul Mehta", "email": "rahul@zenith.edu", "vacancies": 3, "progress": 50, "desc": "Real-time market analytics platform."},
        {"name": "CryptoChain Lite", "lead": "Priya Singh", "email": "priya@zenith.edu", "vacancies": 2, "progress": 35, "desc": "Lightweight blockchain for student transactions."},
    ]
}

# ── ROUTES ───────────────────────────────────────────────
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/index.html')
def home():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        university = request.form.get('university')

        existing = User.query.filter_by(email=email).first()
        if existing:
            flash('Email already registered!')
            return redirect(url_for('register'))

        new_user = User(name=name, email=email, password=password, university=university)
        db.session.add(new_user)
        db.session.commit()

        session['user_email'] = email
        session['user_name'] = name
        return redirect(url_for('dashboard'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email, password=password).first()
        if user:
            session['user_email'] = email
            session['user_name'] = user.name
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password!')
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/dashboard')
def dashboard():
    name = session.get('user_name', 'Scholar')
    user = {"name": name, "level": 4, "rank": "Scholar", "xp": 250}
    stats = {"active_projects": 3, "due_this_week": 2, "xp_this_week": 40, "collaborators": 8, "worlds_count": 2}
    collaborations = [
        {"title": "Neural Interface UI", "world": "Creative Studio", "updated": "Updated 2h ago", "emoji": "🖥️", "icon_bg": "rgba(124,240,168,0.08)", "icon_border": "rgba(124,240,168,0.15)", "status_class": "active", "status_label": "In Progress", "members": [{"initials": "AK", "color": "linear-gradient(135deg,#a78bfa,#60a5fa)"}, {"initials": "RS", "color": "linear-gradient(135deg,#f87171,#fb923c)"}]},
        {"title": "Quantum Data Viz", "world": "Research Lab", "updated": "Updated yesterday", "emoji": "🔬", "icon_bg": "rgba(251,191,36,0.08)", "icon_border": "rgba(251,191,36,0.15)", "status_class": "review", "status_label": "In Review", "members": [{"initials": "DK", "color": "linear-gradient(135deg,#fbbf24,#f87171)"}]},
    ]
    worlds = [
        {"name": "Creative Studio", "color": "#7cf0a8", "members": 12},
        {"name": "Research Lab", "color": "#a78bfa", "members": 8},
        {"name": "Dev Hub", "color": "#fbbf24", "members": 5},
    ]
    recent_messages = [
        {"sender": "Arya K.", "initials": "AK", "avatar_color": "linear-gradient(135deg,#a78bfa,#60a5fa)", "preview": "Can you review the latest commit?", "time": "2m"},
        {"sender": "Ravi S.", "initials": "RS", "avatar_color": "linear-gradient(135deg,#7cf0a8,#60d4f0)", "preview": "The design looks great!", "time": "1h"},
    ]
    return render_template('dashboard.html', user=user, stats=stats, collaborations=collaborations, worlds=worlds, recent_messages=recent_messages, unread_count=2)

@app.route('/worlds')
def worlds():
    worlds_data = [
        {"id": "tech", "title": "The Tech Hub", "match": "94%", "desc": "Software engineering and AI research."},
        {"id": "creative", "title": "Creative Studio", "match": "87%", "desc": "UI/UX design and motion graphics."},
        {"id": "research", "title": "The Lab", "match": "82%", "desc": "Biotech and experimental physics."},
        {"id": "economy", "title": "Economy & Trade", "match": "79%", "desc": "FinTech and market analysis."}
    ]
    return render_template('worlds.html', worlds=worlds_data)

@app.route('/world/<world_id>')
def world_projects(world_id):
    projects = projects_database.get(world_id, [])
    world_display_name = world_id.replace('_', ' ').title()
    return render_template('project_hub.html', projects=projects, world_name=world_display_name)

@app.route('/propose/<world_id>/', methods=['GET', 'POST'])
def propose_project(world_id):
    if request.method == 'POST':
        return redirect(url_for('world_projects', world_id=world_id))
    return render_template('propose_project.html', world_id=world_id)

@app.route('/propose_project', methods=['GET', 'POST'])
def propose_project_page():
    if request.method == 'POST':
        new_project = Project(
            title=request.form.get('title'),
            desc=request.form.get('description'),
            xp=request.form.get('xp') or 100,
            world=request.form.get('world') or 'tech',
            author=session.get('user_name', 'Anonymous'),
            progress=0
        )
        db.session.add(new_project)
        db.session.commit()
        flash('Project proposed successfully!')
        return redirect(url_for('dashboard'))
    return render_template('propose_project.html')

@app.route('/collaborators')
def collaborators():
    total_collabs = User.query.count()
    suggestions = [
        {"name": "Aryan Sharma", "headline": "AI/ML Researcher @ GLA", "skills": ["Python", "TensorFlow", "FastAPI"], "match": "94%"},
        {"name": "Isha Verma", "headline": "UI/UX Designer", "skills": ["Figma", "Three.js", "Adobe XD"], "match": "88%"},
        {"name": "Kabir Das", "headline": "Full Stack Dev", "skills": ["Node.js", "MongoDB", "React"], "match": "82%"}
    ]
    return render_template('collaborators.html', total_collaborators=total_collabs, active_squads=3, suggestions=suggestions)

@app.route('/archive')
def archive():
    archived_data = [
        {"title": "Smart Campus AI", "role": "Lead Developer", "description": "Successfully deployed AI navigation for GLA University."},
        {"title": "Quantum Ledger", "role": "Researcher", "description": "Post-quantum cryptographic standards research."}
    ]
    return render_template('archive.html', archived_projects=archived_data)

@app.route('/messages')
def messages():
    notifications_list = [
        {"type": "join_request", "sender": "Aryan Sharma", "content": "wants to join your squad.", "time": "2m ago", "match": "94%", "project": "Neural Net"},
        {"type": "mission_update", "sender": "System", "content": "Mission 'Database Schema' initialized.", "time": "1h ago", "match": "82%", "project": "Campus Connect"},
        {"type": "announcement", "sender": "Zenith AI", "content": "New teams forming in your domain.", "time": "5h ago", "match": "100%", "project": "Network Hub"}
    ]
    return render_template('messages.html', notifications=notifications_list)

@app.route('/overview')
def overview():
    stats = {"network_size": User.query.count(), "active_missions": Project.query.count(), "collaboration_aura": "98%"}
    steps = [
        {"id": "01", "title": "Neural Entry", "desc": "Login or Register to create your unique student profile."},
        {"id": "02", "title": "Explore Worlds", "desc": "Access AI-driven project worlds and collaborative environments."},
        {"id": "03", "title": "Assemble Squad", "desc": "Connect with collaborators and manage tasks in the Archives."}
    ]
    return render_template('overview.html', stats=stats, steps=steps)

@app.route('/initialize_connection/<name>')
def initialize_connection(name):
    new_size = session.get('network_size', 14) + 1
    session['network_size'] = new_size
    connected = session.get('connected_users', [])
    if name not in connected:
        connected.append(name)
    session['connected_users'] = connected
    flash(f"Connected with {name}!")
    return redirect(url_for('collaborators'))

# ── INIT DB ──────────────────────────────────────────────
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=False)