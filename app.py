import os
import sqlite3
import warnings
import threading
import webbrowser
import tempfile
import shutil
from datetime import datetime
from flask import Flask, render_template, request, jsonify, send_from_directory, abort

app = Flask(__name__)

_secret_key = os.environ.get('SECRET_KEY')
if not _secret_key:
    warnings.warn(
        "SECRET_KEY is not set in environment variables. "
        "Using the default fallback key. Set SECRET_KEY in Vercel project settings for production.",
        stacklevel=1
    )
    _secret_key = 'michael-gertos-portfolio-key-2026'
app.config['SECRET_KEY'] = _secret_key

def _get_database_path():
    # Allow overriding via explicit environment variable
    env_path = os.environ.get('DATABASE_PATH')
    if env_path:
        return env_path

    # On Vercel or AWS Lambda serverless runtimes, the deployment filesystem is read-only.
    # Writable temporary storage must use the system temp directory.
    if os.environ.get('VERCEL') or os.environ.get('AWS_LAMBDA_FUNCTION_NAME') or os.environ.get('NOW_REGION'):
        return os.path.join(tempfile.gettempdir(), 'portfolio.db')

    # Local development default inside workspace database directory
    local_dir = os.path.join(os.path.dirname(__file__), 'database')
    try:
        os.makedirs(local_dir, exist_ok=True)
        test_file = os.path.join(local_dir, '.write_test')
        with open(test_file, 'a') as f:
            pass
        os.remove(test_file)
        return os.path.join(local_dir, 'portfolio.db')
    except (OSError, PermissionError):
        return os.path.join(tempfile.gettempdir(), 'portfolio.db')

DATABASE_PATH = _get_database_path()

def get_db_connection():
    os.makedirs(os.path.dirname(DATABASE_PATH), exist_ok=True)
    seed_db = os.path.join(os.path.dirname(__file__), 'database', 'portfolio.db')
    # In serverless environments, if a pre-existing database file exists, copy it to temp
    if DATABASE_PATH != seed_db and os.path.exists(seed_db) and not os.path.exists(DATABASE_PATH):
        try:
            shutil.copyfile(seed_db, DATABASE_PATH)
        except Exception:
            pass
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contact_messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            subject TEXT,
            message TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            status TEXT DEFAULT 'new'
        )
    ''')
    conn.commit()
    conn.close()

# Personal & Portfolio Data Dictionary (Accurate & Authentic)
PROFILE_DATA = {
    "name": "Michael Angelo Gertos",
    "first_name": "Michael Angelo",
    "nickname": "Michael",
    "titles": [
        "Junior Software Developer",
        "IT Specialist",
        "Full-Stack Developer"
    ],
    "location": "Kalilangan, Bukidnon, Philippines",
    "email": "michaelangelogertos123@gmail.com",
    "phone": "09067224273",
    "github": "https://github.com/kiyoshigertos",
    "tagline": "Building technology that makes work smarter, faster, and more sustainable.",
    "personal_goal": "I want to create systems and technology that make people's jobs easier, faster, and more sustainable.",
    "professional_goal": "Become a Senior Software Developer and eventually establish my own IT company.",
    "about": {
        "summary": "I am an Information Technology student and aspiring software developer with a passion for building practical technology solutions that make people's work easier, faster, and more sustainable.",
        "journey": "During my college journey, I have developed several systems and projects and have also worked on projects for actual clients. I have experience solving practical problems through software and technology.",
        "expansion": "I am currently expanding my skills in Flutter, Python, and Dart while continuously learning new technologies and modern application development approaches.",
        "mindset": "I can work under pressure, collaborate with a team, learn from mentors, and adapt quickly to new engineering challenges.",
        "interests": [
            "Software Development",
            "Systems Architecture",
            "IoT & Automation",
            "Robotics",
            "Computer Hardware",
            "Troubleshooting & Diagnostics",
            "Emerging Technologies"
        ]
    },
    "skills": {
        "programming": [
            {"name": "Python", "desc": "Backend systems, scripting & automation", "category": "Core"},
            {"name": "Dart", "desc": "Strongly typed language for cross-platform apps", "category": "Core"},
            {"name": "Flutter", "desc": "UI toolkit for multi-platform client applications", "category": "Core"}
        ],
        "mobile": [
            {"name": "Flutter Framework", "desc": "Mobile & desktop cross-platform architecture", "category": "Mobile"}
        ],
        "database": [
            {"name": "MySQL", "desc": "Relational database management & SQL querying", "category": "Database"},
            {"name": "Microsoft Access", "desc": "Desktop database design & local record handling", "category": "Database"}
        ],
        "tools": [
            {"name": "Git", "desc": "Version control & collaboration", "category": "Tools"},
            {"name": "GitHub", "desc": "Source code hosting & repository management", "category": "Tools"},
            {"name": "Visual Studio Code", "desc": "Primary code editing environment", "category": "Tools"},
            {"name": "Antigravity", "desc": "Advanced agentic development environment", "category": "Tools"},
            {"name": "Cursor", "desc": "AI-assisted programming IDE", "category": "Tools"}
        ],
        "it_specialist": [
            {"name": "Networking", "desc": "Local network configuration, routing & connectivity diagnostics", "category": "IT / Infra"},
            {"name": "Hardware Troubleshooting", "desc": "Component diagnostics, assembly & repair", "category": "Hardware"},
            {"name": "Software Troubleshooting", "desc": "OS diagnostics, malware remediation & system optimization", "category": "Systems"},
            {"name": "Computer Repair", "desc": "Physical repair, thermal maintenance & device servicing", "category": "Hardware"},
            {"name": "Prompt Engineering", "desc": "Structured LLM prompting & AI agent workflow design", "category": "AI"}
        ],
        "learning": [
            {"name": "Advanced Flutter Architecture", "desc": "State management & production application patterns", "category": "Learning"},
            {"name": "Modern Application Development", "desc": "Cloud integration, microservices & scalable systems", "category": "Learning"}
        ]
    },
    "projects": [
        {
            "id": "smartpos",
            "slug": "smartpos",
            "title": "SmartPOS",
            "type": "Point-of-Sale and Business Management System",
            "badge": "Client-Verified System",
            "category": "Client / Full-Stack",
            "short_description": "A comprehensive POS system built for small businesses to streamline daily sales, track product catalogs, manage inventory, and optimize retail operations across multiple devices.",
            "technologies": ["Flutter", "Python", "Database", "Responsive UI"],
            "image": "smartpos.svg",
            "status": "Deployed & Active Client Use",
            "target_devices": ["Smartphones", "Tablets", "Desktop computers"],
            "clients": [
                {"name": "Jamelo Store", "detail": "Active retail deployment for inventory & daily transactions"},
                {"name": "Hanmae's Store", "detail": "Store inventory management & sales ledger"},
                {"name": "MJMK Convenience Store", "detail": "Point-of-sale terminal for rapid checkout"}
            ],
            "problem": "Small retail and convenience store owners in local communities struggle with manual pen-and-paper ledgers, inaccurate stock accounting, slow checkout lines, and lack of cross-device flexibility.",
            "solution": "Developed SmartPOS with Flutter and Python to provide a responsive, intuitive interface that works on smartphones, tablets, and desktop computers with local database persistence and real-time inventory tracking.",
            "my_role": "Lead Developer & System Architect (System Design, UI Implementation, Database Schema, Client Deployment & Support)",
            "key_features": [
                "Multi-device support across mobile, tablet, and desktop viewports",
                "Product catalog and stock inventory tracking",
                "Fast transaction checkout and sales recording",
                "Daily operations and sales summaries",
                "Responsive UI tailored for quick touch and keyboard workflows"
            ],
            "github_url": "[Repository: Private Client Codebase / Available upon request]",
            "demo_url": "[Client On-Premise Deployments]"
        },
        {
            "id": "elara-ai",
            "slug": "elara-ai",
            "title": "ELARA AI",
            "type": "AI Personal Assistant Project",
            "badge": "AI & Systems Project",
            "category": "AI / Software",
            "tagline": "Don't let ELARA fool you. Let ELARA solve you.",
            "branding_note": "Inspired by the Bisaya term 'elara' (meaning to fool someone), turning the concept into an intelligent assistant that turns complex confusion into clear solutions.",
            "short_description": "An intelligent personal assistant architecture exploring context-aware reasoning, automated scheduling, student workflows, and smart task recommendations.",
            "technologies": ["Python", "Prompt Engineering", "AI Architecture", "System Automation"],
            "image": "elara.svg",
            "status": "In Active Development & Architecture Phase",
            "problem": "Students and professionals face fragmented digital tools, inefficient task management, and information overload when juggling coursework, schedules, and technical workflows.",
            "solution": "Architecting ELARA as a modular assistant capable of handling conversational logic, document queries, and productivity recommendations with high privacy and reliability.",
            "my_role": "Creator & Lead Developer (System Architecture, Prompt Logic, Interaction Design)",
            "feature_breakdown": {
                "implemented": [
                    "Core conversational interface and command parsing pipeline",
                    "Structured prompt engineering workflows and persona logic",
                    "Interactive CLI and modular response dispatcher"
                ],
                "planned": [
                    "Multilingual Bisaya, Tagalog, and English conversational understanding",
                    "Student academic workflow & study schedule optimization",
                    "Automated document analysis and contextual summarization",
                    "Intelligent daily recommendations & habit tracking",
                    "Offline-capable local inference module"
                ],
                "experimental": [
                    "Voice input/output speech processing pipelines",
                    "Context-sensitive emotional intelligence heuristics",
                    "Cross-application and OS-level automated task interaction"
                ]
            },
            "github_url": "[Repository: In Active Development / Placeholder]",
            "demo_url": "[Prototype Stage / Demonstration Preview Available]"
        },
        {
            "id": "smart-bin",
            "slug": "smart-bin",
            "title": "Smart Bin",
            "type": "IoT / Smart Waste Management",
            "badge": "IoT & Sustainability",
            "category": "IoT / Hardware",
            "short_description": "An IoT-focused smart waste monitoring and automated management system designed to improve sanitation efficiency and environmental sustainability.",
            "technologies": ["IoT Architecture", "Hardware & Microcontroller [Placeholder]", "Sensors [Placeholder]", "Automation"],
            "image": "smartbin.svg",
            "status": "Prototype & Engineering Concept",
            "problem": "Traditional waste disposal often suffers from overflowing bins, inefficient manual collection schedules, and lack of real-time fill-level visibility in institutional environments.",
            "solution": "Designed a connected waste management concept integrating hardware sensing, automated level monitoring, and status reporting to optimize waste collection timing and promote sustainable campus sanitation.",
            "my_role": "Hardware-Software Integrator & Project Co-Developer",
            "key_features": [
                "Real-time waste fill-level monitoring framework",
                "Automated status indication and notification pipeline",
                "Focus on environmental sustainability and municipal efficiency",
                "Hardware/sensor integration placeholder for configurable sensor arrays [Ultrasonic / Weight / Infrared]"
            ],
            "technical_specs": {
                "microcontroller": "[Hardware Specification Placeholder - e.g., Arduino / ESP32]",
                "sensors": "[Sensors Array Placeholder - e.g., Distance/Level Sensors]",
                "connectivity": "[Communication Protocol Placeholder - e.g., Wi-Fi / Serial]"
            },
            "github_url": "[Repository Placeholder]",
            "demo_url": "[Project Showcase Placeholder]"
        },
        {
            "id": "space-dodger",
            "slug": "space-dodger",
            "title": "Space Dodger",
            "type": "2D Game Project",
            "badge": "Game Logic & Mechanics",
            "category": "Game Dev / Logic",
            "short_description": "A 2D space-themed arcade game built to demonstrate core programming logic, real-time collision detection, responsive keyboard controls, scoring systems, and dynamic game loops.",
            "technologies": ["Programming Logic", "Game Loop Architecture", "[Game Engine Placeholder]", "[Language Placeholder]"],
            "image": "space_dodger.svg",
            "status": "Completed Academic / Logic Demonstration Project",
            "problem": "Mastering interactive state management, tick-based rendering loops, and real-time obstacle physics requires robust mathematical logic and tight input handling.",
            "solution": "Engineered an engaging arcade game featuring continuous obstacle spawning, hit-box collision calculations, progressive difficulty scaling, and high-score retention.",
            "my_role": "Solo Game Logic & Gameplay Developer",
            "key_features": [
                "Real-time 2D spatial coordinate tracking and collision calculations",
                "Smooth keyboard input handling and player maneuverability",
                "Progressive speed and obstacle difficulty curve",
                "Scoring system and session high-score persistence"
            ],
            "technical_specs": {
                "engine": "[Game Engine Placeholder]",
                "language": "[Programming Language Placeholder]",
                "graphics": "2D Retro Arcade Assets & Particle Effects"
            },
            "github_url": "[Repository Placeholder]",
            "demo_url": "[Playable Demo Placeholder]"
        }
    ],
    "experience": [
        {
            "role": "Freelance Software Developer",
            "company": "Independent Client Work",
            "location": "Bukidnon, Philippines",
            "period": "Client Engagements",
            "type": "Client Development",
            "highlight": "Delivered SmartPOS to real-world store owners",
            "responsibilities": [
                "Engaged directly with retail business owners to gather workflow requirements and point-of-sale pain points.",
                "Architected and implemented SmartPOS for Jamelo Store, Hanmae's Store, and MJMK Convenience Store.",
                "Created responsive interfaces tailored for tablet, mobile, and desktop operating environments.",
                "Handled database setup, inventory tracking structures, and client deployment on-site."
            ],
            "clients": ["Jamelo Store", "Hanmae's Store", "MJMK Convenience Store"]
        },
        {
            "role": "Assistant Technician",
            "company": "Harvey's Electronic and Repair Shop and Services",
            "location": "Kalilangan, Bukidnon, Philippines",
            "period": "September 2023 - February 2024",
            "type": "Technical Service & Diagnostics",
            "highlight": "Practical hardware/software troubleshooting & customer device care",
            "responsibilities": [
                "Conducted direct client intake interviews to accurately assess computer and electronic device issues.",
                "Assisted in identifying root hardware faults, component degradation, and operating system errors.",
                "Performed systematic hardware and software diagnostics using professional troubleshooting and repair tools.",
                "Successfully remediated and recovered severely virus-infected and corrupted laptop systems.",
                "Executed hardware replacements, thermal servicing, and preventive maintenance on client machines."
            ]
        }
    ],
    "education": {
        "institution": "Torres Capitol College, Inc.",
        "institution_alt": "Formerly Philippine Countryville College, Inc. | Maramag, Bukidnon",
        "degree": "Bachelor of Science in Information Technology",
        "period": "2024 - Present",
        "status": "Currently Pursuing (BSIT)",
        "leadership": "PIO — IT Department Student Organization, Torres Capitol College, Inc.",
        "academic_achievements": [
            "3x Consecutive Dean's Lister (AY 24-25 1st Sem: 1.42 | AY 24-25 2nd Sem: 1.56 | AY 25-26 1st Sem: 1.72)",
            "Latin Award Candidate / Nominee",
            "Best Programmer Award",
            "Capstone of the Year",
            "Academic Excellence with Honors (DepEd Kalilangan NHS - 90% GWA)"
        ]
    },
    "achievements": [
        {
            "id": "robotics-champ",
            "year": "2025",
            "title": "Robotics Championship — Champion",
            "organization": "Torres Capitol College, Inc. (formerly Philippine Countryville College)",
            "description": "Led robotics design, circuit automation, and algorithmic control logic to secure 1st place in the institutional engineering challenge.",
            "category": "competition"
        },
        {
            "id": "hackathon-1st",
            "year": "2024",
            "title": "Hackathon — 1st Place Champion",
            "organization": "Torres Capitol College, Inc. (formerly Philippine Countryville College)",
            "description": "Developed an innovative software solution under rapid time constraints, demonstrating rapid systems design and clean architecture.",
            "category": "competition"
        },
        {
            "id": "arnis-1st",
            "year": "2025",
            "title": "Sayaw Arnis / Kali — 1st Place",
            "organization": "Torres Capitol College, Inc. (formerly Philippine Countryville College)",
            "description": "Recognized for physical discipline, traditional martial arts coordination, and precision execution.",
            "category": "competition"
        }
    ],
    "certifications": [
        {
            "id": "tcc-deans-list-1-2026",
            "title": "Dean's List Certificate of Recognition — 1st Semester AY 2025–2026",
            "short_title": "Dean's List (AY 25-26)",
            "issuer": "Torres Capitol College, Inc. — School of Information Technology",
            "issuer_short": "Torres Capitol College",
            "category": "academic",
            "category_label": "Academic Distinction",
            "year": "2026",
            "issued_date": "March 6, 2026",
            "gwa": "1.72 General Average (Dean's List)",
            "badge": "Dean's Lister (1.72 GWA)",
            "signatory": "April Jean D. Villas (BSIT Program Head), Roxanne Jayn-Lesley M. Marpa, Arnel V. Bangis, DM, Dr. Fe A. Torres, Ph.D., Feelin Torres-Jumamil, MAN, RN",
            "image": "certificates/tcc_deans_list_1st_sem_2025_2026.jpg",
            "highlight": "Awarded for achieving an outstanding general average of 1.72 during the First Semester of AY 2025-2026 and qualifying for inclusion in the esteemed Dean's List.",
            "skills_covered": [
                "Advanced Systems Architecture & Logic",
                "Cross-Platform Software Engineering",
                "Scholastic Discipline & Academic Excellence",
                "3x Consecutive Dean's Honor Standing"
            ]
        },
        {
            "id": "tesda-nc2-css",
            "title": "National Certificate II in Computer Systems Servicing (CSS NC II)",
            "short_title": "TESDA CSS NC II",
            "issuer": "Technical Education and Skills Development Authority (TESDA)",
            "issuer_short": "TESDA",
            "category": "national",
            "category_label": "National Government Certificate",
            "year": "2024",
            "issued_date": "February 22, 2024",
            "validity": "Valid until February 21, 2029",
            "cert_no": "24101302001324",
            "uli": "ULI-GMR-05-023-10013-001",
            "badge": "National Certificate II",
            "signatory": "Sec. Suharto T. Mangudadatu, Ph.D. (TESDA Director General)",
            "image": "certificates/tesda_nc2_computer_systems_servicing.jpg",
            "highlight": "Officially certified in computer hardware assembly, OS installation, network cabling, server administration, and diagnostic repair.",
            "skills_covered": [
                "Install & Configure Computer Systems",
                "Set-up Computer Networks & Cabling",
                "Set-up & Maintain Computer Servers",
                "Maintain & Repair Computer Systems & Networks",
                "Terminate & Connect Electrical Wiring & Electronic Circuits",
                "Test Electronic Components & Circuitry",
                "Occupational Health & Workplace Safety Standards"
            ]
        },
        {
            "id": "pcc-deans-list-1",
            "title": "Dean's List Certificate — 1st Semester AY 2024–2025",
            "short_title": "Dean's List (1st Sem)",
            "issuer": "Philippine Countryville College, Inc. (now Torres Capitol College) — School of IT",
            "issuer_short": "PCC / Torres Capitol College",
            "category": "academic",
            "category_label": "Academic Distinction",
            "year": "2025",
            "issued_date": "April 11, 2025",
            "gwa": "1.42 (Academic Distinction)",
            "badge": "Dean's Lister (1.42 GWA)",
            "signatory": "April Jean D. Villas (BSIT Program Head), Dr. Fe A. Torres, PhD, Dr. Gordon M. Torres, EDL",
            "image": "certificates/deans_list_1st_sem_2024_2025.jpg",
            "highlight": "Conferred for outstanding scholastic performance and maintaining an exemplary grade weighted average of 1.42 in BSIT coursework.",
            "skills_covered": [
                "Advanced Programming & Algorithms",
                "Information Management & Database Systems",
                "Academic Rigor & Theoretical CS Foundation",
                "Top-Tier Academic Ranking"
            ]
        },
        {
            "id": "pcc-deans-list-2",
            "title": "Dean's List Certificate — 2nd Semester AY 2024–2025",
            "short_title": "Dean's List (2nd Sem)",
            "issuer": "Philippine Countryville College, Inc. (now Torres Capitol College) — School of IT",
            "issuer_short": "PCC / Torres Capitol College",
            "category": "academic",
            "category_label": "Academic Distinction",
            "year": "2025",
            "issued_date": "October 3, 2025",
            "gwa": "1.56 (Academic Distinction)",
            "badge": "Dean's Lister (1.56 GWA)",
            "signatory": "April Jean D. Villas (BSIT Program Head), Sarah D. Estorgio, Feelin Torres-Jumamil, DM",
            "image": "certificates/deans_list_2nd_sem_2024_2025.jpg",
            "highlight": "Conferred for consecutive academic excellence, achieving a 1.56 grade weighted average during the second semester of BSIT.",
            "skills_covered": [
                "Full-Stack Software Engineering",
                "Object-Oriented Design & Application Development",
                "Consecutive Academic Honor Standing",
                "Systems Analysis & Project Execution"
            ]
        },

        {
            "id": "pcc-gameplay-defense",
            "title": "Certificate of Participation — Gameplay Defense",
            "short_title": "BSIT Gameplay Defense",
            "issuer": "Philippine Countryville College, Inc. — BSIT Program",
            "issuer_short": "PCC BSIT Program",
            "category": "seminar",
            "category_label": "Academic & Project Defense",
            "year": "2025",
            "issued_date": "May 8, 2025",
            "badge": "Technical Defense",
            "signatory": "Cindy Briel E. Torres (BSIT Instructor), April Jean D. Villas (BSIT Program Head)",
            "image": "certificates/pcc_gameplay_defense.jpg",
            "highlight": "Recognized for successfully defending interactive game systems and interactive logic at the College Library Administration Building.",
            "skills_covered": [
                "2D Game Architecture & Gameplay Loop",
                "Real-Time Physics & Collision Detection",
                "Technical Project Defense & Live Demonstration",
                "Interactive UI & Input Handling Logic"
            ]
        },
        {
            "id": "dict-cybersecurity-seminar",
            "title": "BSIT Seminar-Workshop: Digital Danger Zone — Protecting Yourself in the Age of Digital Deception",
            "short_title": "DICT Cybersecurity Seminar",
            "issuer": "Department of Information and Communications Technology (DICT Region 10) & PCC",
            "issuer_short": "DICT Region 10 / PCC",
            "category": "seminar",
            "category_label": "Cybersecurity & Industry Training",
            "year": "2025",
            "issued_date": "Academic Year 2024-2025",
            "badge": "DICT / Cybersecurity",
            "signatory": "Keren Happuch Lacadin (Project Lead, DICT Region 10), April Jean D. Villas, Dr. Gordon M. Torres",
            "image": "certificates/dict_cybersecurity_seminar.jpg",
            "highlight": "Specialized training on threat analysis, digital security defense, social engineering awareness, and information security counter-measures.",
            "skills_covered": [
                "Information Security & Cyber Defense",
                "Social Engineering & Phishing Prevention",
                "Data Privacy Protection Protocols",
                "Industry ICT Security Standards"
            ]
        },
        {
            "id": "deped-kalilangan-honors",
            "title": "Certificate of Recognition — Academic Excellence With Honors",
            "short_title": "Academic Excellence With Honors",
            "issuer": "Department of Education (DepEd-ROX) — Kalilangan National High School",
            "issuer_short": "DepEd / Kalilangan NHS",
            "category": "academic",
            "category_label": "Secondary Academic Honor",
            "year": "2023",
            "issued_date": "February 17, 2023",
            "gwa": "90% Grade Average",
            "badge": "With Honors (90% Average)",
            "signatory": "Jerg Michael G. Rosell (Adviser), Jennifer M. Dulla (School Principal II), Dr. Juhemar C. Cantones",
            "image": "certificates/deped_academic_excellence_honors.jpg",
            "highlight": "Conferred by the Department of Education for obtaining an average grade of 90% and distinguished academic performance in curricular activities.",
            "skills_covered": [
                "Foundational STEM & Mathematics",
                "Curricular Leadership & School Organization",
                "Scholastic Diligence & Academic Excellence"
            ]
        },
        {
            "id": "devcon-bukidnon",
            "title": "Certificate of Participation — DEVCON Bits of Light Roadshow (Frontend Forge Workshop)",
            "short_title": "DevCon Bits of Light 2026",
            "issuer": "DEVCON Bukidnon Chapter & DICT Region X — Campus DevCon @ Torres Capitol College",
            "issuer_short": "DEVCON Bukidnon / DICT Region X",
            "category": "seminar",
            "category_label": "Developer Conference & Workshop",
            "year": "2026",
            "issued_date": "July 30, 2026",
            "badge": "DEVCON Bits of Light",
            "signatory": "Glyrhiz Marhiel A. Tabamo (President, DEVCON Bukidnon Chapter), Mark Ian Hendrez (Engineer, DICT Region X)",
            "image": "certificates/devcon_bits_of_light_2026.jpg",
            "highlight": "Recognized for active participation in the Frontend Forge workshop during the DEVCON Bits of Light Roadshow: A Day of Learning, Care, and Smiles \u2014 themed 'Spreading Light Through Technology and Compassion,' held at Torres Capitol College, Inc., Maramag, Bukidnon.",
            "skills_covered": [
                "Micro Robotics & Hardware Bot Building",
                "Block-Based & Visual Programming Logic",
                "Problem Solving & Computational Thinking",
                "Frontend Development Fundamentals",
                "Developer Community Collaboration & Industry Networking"
            ]
        }
    ]
}

# Routes
@app.route('/')
def index():
    return render_template('index.html', profile=PROFILE_DATA)

@app.route('/projects')
def projects_page():
    return render_template('projects.html', profile=PROFILE_DATA)

@app.route('/project/<slug>')
def project_detail(slug):
    project = next((p for p in PROFILE_DATA['projects'] if p['slug'] == slug), None)
    if not project:
        abort(404)
    return render_template('project_detail.html', profile=PROFILE_DATA, project=project)

@app.route('/api/projects')
def api_projects():
    return jsonify(PROFILE_DATA['projects'])

@app.route('/api/project/<slug>')
def api_project_detail(slug):
    project = next((p for p in PROFILE_DATA['projects'] if p['slug'] == slug), None)
    if not project:
        return jsonify({"status": "error", "message": "Project not found"}), 404
    return jsonify({"status": "success", "project": project})

@app.route('/api/certifications')
def api_certifications():
    return jsonify(PROFILE_DATA['certifications'])

@app.route('/api/certifications/<cert_id>')
def api_certification_detail(cert_id):
    cert = next((c for c in PROFILE_DATA['certifications'] if c.get('id') == cert_id), None)
    if not cert:
        return jsonify({"status": "error", "message": "Certification not found"}), 404
    return jsonify({"status": "success", "certification": cert})



@app.route('/api/contact', methods=['POST'])
def contact_submit():
    data = request.get_json() if request.is_json else request.form
    name = (data.get('name') or '').strip()
    email = (data.get('email') or '').strip()
    subject = (data.get('subject') or 'Portfolio Contact Inquiry').strip()
    message = (data.get('message') or '').strip()

    if not name or not email or not message:
        return jsonify({
            'status': 'error',
            'message': 'Please fill in all required fields (Name, Email, Message).'
        }), 400

    if '@' not in email or '.' not in email:
        return jsonify({
            'status': 'error',
            'message': 'Please provide a valid email address.'
        }), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO contact_messages (name, email, subject, message) VALUES (?, ?, ?, ?)',
            (name, email, subject, message)
        )
        conn.commit()
        conn.close()

        return jsonify({
            'status': 'success',
            'message': f"Thank you, {name}! Your message has been recorded. Michael will reach back to you at {email}."
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f"Unable to save message: {str(e)}"
        }), 500

@app.route('/download-resume')
def download_resume():
    files_dir = os.path.join(app.static_folder, 'files')
    filename = 'Michael_Angelo_Gertos_Resume.pdf'
    filepath = os.path.join(files_dir, filename)
    if os.path.exists(filepath):
        return send_from_directory(files_dir, filename, as_attachment=True)
    # If the file hasn't been placed, redirect or display friendly notice
    abort(404)

@app.route('/favicon.ico')
def favicon():
    images_dir = os.path.join(app.static_folder, 'images')
    return send_from_directory(images_dir, 'favicon.svg', mimetype='image/svg+xml')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', profile=PROFILE_DATA), 404

@app.errorhandler(500)
def server_error(e):
    return render_template('500.html', profile=PROFILE_DATA), 500

# Initialize the database on startup (resilient for serverless environments)
try:
    with app.app_context():
        init_db()
except Exception as e:
    app.logger.warning(f"Database auto-initialization deferred: {e}")

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    url = f'http://127.0.0.1:{port}'

    # Register Brave as the browser; fall back to system default if not found.
    brave_path = r'C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe'
    try:
        webbrowser.register(
            'brave',
            None,
            webbrowser.BackgroundBrowser(brave_path)
        )
        browser = webbrowser.get('brave')
    except Exception:
        browser = webbrowser.get()

    # Open the browser 1 second after Flask starts (gives the server time to bind).
    threading.Timer(1.0, lambda: browser.open(url)).start()

    app.run(host='127.0.0.1', port=port, debug=False)

