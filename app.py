from flask import Flask, render_template, request, redirect, url_for , session

app = Flask(__name__)
app.secret_key = 'your_secret_key_here' # Add this line

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
        # 1. Collect data from the Register form
        email = request.form.get('email')
        name = request.form.get('name')
        password = request.form.get('password')
       
        # 2. Save user to MongoDB (initial record)
        # Assuming you use mongo.db.users.insert_one({...})
       
        # 3. Store email in session to identify the user on the next page
        session['user_email'] = email
       
        # 4. REDIRECT to the niche page automatically
        return redirect(url_for('select_niche'))
       
    return render_template('register.html')

@app.route('/niche')
def select_niche():
    # This renders the new dynamic niche page you created
    return render_template('niche.html')

# 1. The Niche Selection Handler
@app.route('/save_niche', methods=['POST'])
def save_niche():
    selected = request.form.get('selected_niche')
    session['user_niche'] = selected  # Store selection in session
   
    # Map the display name to a clean URL slug
    niche_slugs = {
        "Web Development": "web-dev",
        "AI/ML": "ai-ml",
        "Cloud Computing": "cloud",
        "UI/UX Design": "design"
    }
   
    slug = niche_slugs.get(selected, "general")
    return redirect(url_for('project_hub', niche_slug=slug))

@app.route('/projects/<niche_slug>')
def project_hub(niche_slug):
    # Mapping slugs to display names and colors
    niche_configs = {
        "web-dev": {"name": "Web Development", "color": "#6366f1"},
        "ai-ml": {"name": "AI/ML", "color": "#a855f7"},
        "cloud": {"name": "Cloud Computing", "color": "#00d2ff"},
        "design": {"name": "UI/UX Design", "color": "#f43f5e"}
    }
   
    config = niche_configs.get(niche_slug, {"name": "General", "color": "#ffffff"})
   
    # Example Project Data (In a real app, fetch these from MongoDB)
    # This aligns with your AI Interviewer and Neural Interface projects
    all_projects = [
        {
            "name": "AI Interviewer",
            "description": "Utilizing Groq API and MongoDB to automate student vetting.",
            "niche": "ai-ml",
            "slots": 2,
            "duration": "4 Weeks",
            "status": "Active Mission"
        },
        {
            "name": "Neural Interface UI",
            "description": "Building high-fidelity collaboration dashboards for task coordination.",
            "niche": "web-dev",
            "slots": 3,
            "duration": "2 Weeks",
            "status": "Design Phase"
        },
        {
            "name": "Azure Scalability Lab",
            "description": "Testing VMSS and Availability Sets for high-load coordination.",
            "niche": "cloud",
            "slots": 5,
            "duration": "1 Week",
            "status": "Experimental"
        }
    ]
   
    # Filter projects based on the current niche
    filtered_projects = [p for p in all_projects if p['niche'] == niche_slug]
   
    return render_template('projects.html',
                           niche_name=config['name'],
                           niche_color=config['color'],
                           projects=filtered_projects)
@app.route('/propose-project')
def propose_projects():
    # This renders the 'Tech Hub' page from your second picture
    return render_template('propose_project.html')

@app.route('/project/<project_id>')
def project_detail(project_id):
    # In a real app, you would do: project = mongo.db.projects.find_one({"_id": ObjectId(project_id)})
    # For now, here is a placeholder based on your UI:
    project = {
        "title": "Neural Interface UI",
        "overview": "Building high-fidelity collaboration dashboards for task coordination.",
        "leader_name": "Kavyansh Kulshrestha", # From your project leads
        "leader_email": "lead@university.edu",
        "members": ["Etiksha Jain", "Prince Yadav", "Shiva Dixit"],
        "vacancies": 3,
        "progress": 45,
        "phase": "Design Phase"
    }
    return render_template('project_overview.html', project=project)

@app.route('/join_project/<project_id>', methods=['POST'])
def join_project(project_id):
    # Perform your database logic here (e.g., adding user to request list)
    return {'status': 'success'}, 200

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