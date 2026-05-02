from flask import Flask, render_template, request, redirect, url_for , session, flash

app = Flask(__name__)
app.secret_key = 'your_secret_key'

@app.route('/authenticate', methods=['POST'])
def authenticate():
    email = request.form.get('email')
    password = request.form.get('password')

    # 1. Validate College Domain
    if not email or not email.endswith('@gla.ac.in'):
        return "Access Denied: Use your @gla.ac.in email."

    # 2. Check Password Prefix
    # This ensures the password begins with 125158
    if password and password.startswith('125158'):
        # Optional: Check for a minimum length (e.g., prefix + at least 1 more character)
        if len(password) > 6:
            session['user_email'] = email
            return redirect(url_for('dashboard'))
        else:
            return "rollno. too short! Must have extra characters."
    
    else:
        return "Invalid Roll no.!"

@app.route('/initialize_connection/<name>')
def initialize_connection(name):
    # Grab the current size, add 1, and save it back to 'network_size'
    new_size = session.get('network_size', 14) + 1
    session['network_size'] = new_size

    connected = session.get('connected_users', [])
    if name not in connected:
        connected.append(name)
    session['connected_users'] = connected

    # 3. Flash the success message
    flash(f"Made new connection with {name}!")
    
    # Send user back to collaborators page
    return redirect(url_for('collaborators'))

@app.route('/')
def index():
    return render_template('index.html')

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
    "lab": [
        {"name": "Quantum Data Viz", "lead": "Dr. Aris", "email": "aris@zenith.edu", "vacancies": 1, "progress": 40, "desc": "Multi-dimensional sets."},
        {"name": "Bio-Polymer Synthesis", "lead": "Liam Chen", "email": "liam@zenith.edu", "vacancies": 4, "progress": 10, "desc": "Eco-friendly plastic alternatives."},
        {"name": "Fusion Analytics", "lead": "Elena Rossi", "email": "elena@zenith.edu", "vacancies": 2, "progress": 75, "desc": "Plasma stability prediction models."}
    ]
}
@app.route('/propose/<world_id>/', methods=['GET', 'POST'])
def propose_project(world_id):

    if request.method == 'POST':
        # Logic to handle the form data would go here
        return redirect(url_for('world_projects', world_id=world_id))
    return render_template('propose_project.html', world_id=world_id)
# MISSING REGISTER ROUTE: Add this to fix the BuildError
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        return redirect(url_for('dashboard'))
    return render_template('register.html')

@app.route('/world/<world_id>')
def world_projects(world_id):
    # Fixed the variable name here to avoid the NameError
    projects = projects_database.get(world_id, []) 
    world_display_name = world_id.replace('_', ' ').title()
    return render_template('project_hub.html', projects=projects, world_name=world_display_name)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/worlds')
def worlds():
    worlds_data = [
        # Added "id" to each dictionary so the URL knows where to go
        {"id": "tech", "title": "The Tech Hub", "match": "94%", "desc": "Software engineering and AI research."},
        {"id": "creative", "title": "Creative Studio", "match": "87%", "desc": "UI/UX design and motion graphics."},
        {"id": "research", "title": "The Lab", "match": "82%", "desc": "Biotech and experimental physics."},
        {"id": "economy", "title": "Economy & Trade", "match": "79%", "desc": "FinTech and market analysis."}
    ]
    return render_template('worlds.html', worlds=worlds_data)

# ── Add this to your app.py ──
# This shows how to pass the right data to dashboard.html

@app.route('/dashboard')
def dashboard():
    # Replace with your actual DB queries / session data
    user = {
        "name": "Scholar",
        "level": 4,
        "rank": "Scholar",
        "xp": 250,
    }

    stats = {
        "active_projects": 3,
        "due_this_week": 2,
        "xp_this_week": 40,
        "collaborators": 8,
        "worlds_count": 2,
    }

    collaborations = [
        {
            "title": "Neural Interface UI",
            "world": "Creative Studio",
            "updated": "Updated 2h ago",
            "emoji": "🖥️",
            "icon_bg": "rgba(124,240,168,0.08)",
            "icon_border": "rgba(124,240,168,0.15)",
            "status_class": "active",
            "status_label": "In Progress",
            "members": [
                {"initials": "AK", "color": "linear-gradient(135deg,#a78bfa,#60a5fa)"},
                {"initials": "RS", "color": "linear-gradient(135deg,#f87171,#fb923c)"},
                {"initials": "PM", "color": "linear-gradient(135deg,#7cf0a8,#60d4f0)"},
            ],
        },
        {
            "title": "Quantum Data Viz",
            "world": "Research Lab",
            "updated": "Updated yesterday",
            "emoji": "🔬",
            "icon_bg": "rgba(251,191,36,0.08)",
            "icon_border": "rgba(251,191,36,0.15)",
            "status_class": "review",
            "status_label": "In Review",
            "members": [
                {"initials": "DK", "color": "linear-gradient(135deg,#fbbf24,#f87171)"},
                {"initials": "EL", "color": "linear-gradient(135deg,#60a5fa,#a78bfa)"},
            ],
        },
    ]

    worlds = [
        {"name": "Creative Studio", "color": "#7cf0a8", "members": 12},
        {"name": "Research Lab",    "color": "#a78bfa", "members": 8},
        {"name": "Art District",    "color": "#60a5fa", "members": 20},
        {"name": "Dev Hub",         "color": "#fbbf24", "members": 5},
    ]

    recent_messages = [
        {
            "sender": "Arya K.",
            "initials": "AK",
            "avatar_color": "linear-gradient(135deg,#a78bfa,#60a5fa)",
            "preview": "Can you review the latest commit?",
            "time": "2m",
        },
        {
            "sender": "Ravi S.",
            "initials": "RS",
            "avatar_color": "linear-gradient(135deg,#7cf0a8,#60d4f0)",
            "preview": "The design looks great! Merging now.",
            "time": "1h",
        },
        {
            "sender": "Priya M.",
            "initials": "PM",
            "avatar_color": "linear-gradient(135deg,#fbbf24,#f87171)",
            "preview": "Meeting at 4PM today for Quantum Viz",
            "time": "3h",
        },
    ]

    unread_count = 3

    return render_template(
        'dashboard.html',
        user=user,
        stats=stats,
        collaborations=collaborations,
        worlds=worlds,
        recent_messages=recent_messages,
        unread_count=unread_count,
    )



@app.route('/archive')
def archive():
    # Keep the logic below, but remove the 'if' check above
    archived_data = [
        {
            "title": "Smart Campus AI",
            "role": "Lead Developer",
            "description": "Successfully deployed AI navigation for GLA University."
        }
    ]
    return render_template('archive.html', archived_projects=archived_data)

@app.route('/collaborators')
def collaborators():
    # 1. Security Check
    

    # 2. Mock Data for Collaborators (Connect these to your DB later)
    total_collabs = 14
    active_squads = 3
    
    # 3. AI Suggestions logic
    suggestions = [
        {
            "name": "Aryan Sharma",
            "headline": "AI/ML Researcher @ GLA",
            "skills": ["Python", "TensorFlow", "FastAPI"],
            "match": "94%"
        },
        {
            "name": "Isha Verma",
            "headline": "UI/UX Designer",
            "skills": ["Figma", "Three.js", "Adobe XD"],
            "match": "88%"
        },
        {
            "name": "Kabir Das",
            "headline": "Full Stack Dev",
            "skills": ["Node.js", "MongoDB", "React"],
            "match": "82%"
        }
    ]

    return render_template('collaborators.html', 
                           total_collaborators=total_collabs, 
                           active_squads=active_squads,
                           suggestions=suggestions)

# At the top of your app.py, make sure you have a list to store projects
projects_db = [] 

@app.route('/propose_project', methods=['GET', 'POST'])
def propose_project_page():
    if request.method == 'POST':
        # Get data from the form
        new_project = {
            "title": request.form.get('title'),
            "desc": request.form.get('description'),
            "xp": request.form.get('xp'),
            "world": request.form.get('world'),
            "author": "Nandini Saraswat", # Default lead
            "progress": 0
        }
        projects_db.append(new_project)
        return redirect(url_for('index')) # Redirect back to dashboard
    
    return render_template('propose_project.html')

@app.route('/index.html')
def home():
    return render_template('index.html')
@app.route('/overview')
def overview():
    stats = {"network_size": 14, "active_missions": 3, "collaboration_aura": "98%"}
    
    # Platform Access Steps
    steps = [
        {"id": "01", "title": "Neural Entry", "desc": "Login or Register to create your unique student profile."},
        {"id": "02", "title": "Explore Worlds", "desc": "Access AI-driven project worlds and collaborative environments."},
        {"id": "03", "title": "Assemble Squad", "desc": "Connect with collaborators and manage tasks in the Archives."}
    ]
    
    return render_template('overview.html', stats=stats, steps=steps)

@app.route('/messages')
def messages():
    # Ye data list aapke database se bhi aa sakti hai
    # Filhal hum ise dynamic mock data ke taur par use kar rahe hain
    notifications_list = [
        {
            "type": "join_request",
            "sender": "Aryan Sharma",
            "content": "wants to join your squad as an AI/ML Researcher.",
            "time": "2m ago",
            "match": "94%",
            "project": "Neural Net"
        },
        {
            "type": "mission_update",
            "sender": "System",
            "content": "Mission 'Database Schema' has been successfully initialized.",
            "time": "1h ago",
            "match": "82%",
            "project": "Campus Connect"
        },
        {
            "type": "announcement",
            "sender": "Zenith AI",
            "content": "New interest-based teams are forming in your domain. Check your dashboard.",
            "time": "5h ago",
            "match": "100%",
            "project": "Network Hub"
        }
    ]
    
    return render_template('messages.html', notifications=notifications_list)

if __name__ == '__main__':
    app.run(debug=True)