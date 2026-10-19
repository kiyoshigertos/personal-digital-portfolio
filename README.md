# Michael Angelo Gertos — Personal Digital Portfolio

A professional, high-performance personal digital portfolio website for **Michael Angelo Gertos**, Junior Software Developer, IT Specialist, and Full-Stack Developer based in Kalilangan, Bukidnon, Philippines.

Built with **Python (Flask)**, **SQLite**, **HTML5 Semantic Architecture**, **Modern Vanilla CSS (Custom Design System)**, and **JavaScript (Modular Interaction Engine)**.

---

## 🌟 Key Features

- **Modern Dark Tech Aesthetic**: Engineered with deep charcoal backgrounds, sleek glassmorphism, responsive grid architecture, and refined glowing accent layers.
- **Authentic Portfolio Data**: Accurately showcases real-world client deployments (SmartPOS with 3 active retail clients), competitive robotics and hackathon championships, hardware diagnostics experience, and academic distinctions without exaggerations or fake statistics.
- **Dynamic Typing Engine**: Smoothly rotates between professional titles in the hero section.
- **Domain-Filtered Skills Showcase**: Categorizes core programming, mobile architecture, databases, developer tools, IT troubleshooting, and learning tracks with zero arbitrary percentage bars.
- **Featured Systems & Interactive Modal**:
  - **SmartPOS**: Real-world Point-of-Sale and inventory management system for local stores.
  - **ELARA AI**: AI Assistant project with reverse-psychology branding and distinct Implemented vs Planned vs Experimental lifecycle stages.
  - **Smart Bin**: IoT smart waste monitoring and sustainability prototype.
  - **Space Dodger**: 2D arcade game demonstrating programming logic, collision physics, and game loops.
  - Interactive quick modal previews + dedicated deep-dive case study routes (`/project/<slug>`).
- **Functional Contact Engine**: SQLite-backed contact inquiry API (`/api/contact`) with frontend validation, loading states, and toast notifications.
- **Official Resume Generation**: Includes a downloadable PDF resume (`/download-resume`) built with authentic credentials.
- **Fully Responsive & Accessible**: Custom mobile navigation drawer, skip-links, ARIA landmarks, and `prefers-reduced-motion` compliance.

---

## 📂 Project Architecture

```
Personal Digital Portfolio/
│
├── app.py                      # Flask Application, Routes, SQLite DB Initialization, API Endpoints
├── requirements.txt            # Python Dependencies (Flask, reportlab)
├── vercel.json                 # Vercel Production Deployment & Routing Configuration
├── generate_resume_pdf.py      # Automated Resume PDF Generator
├── README.md                   # Technical Documentation & Instructions
├── test_app.py                 # Comprehensive Automated Test Suite
│
├── api/
│   └── index.py                # Serverless Function WSGI Entrypoint for Vercel
│
├── database/
│   └── portfolio.db            # SQLite Database (Stores contact submissions & messages)
│
├── templates/
│   ├── base.html               # Global Layout, Navigation, Modals, SEO & Footers
│   ├── index.html              # Main Landing Page (Hero, About, Skills, Projects, Experience, Education, Achievements, Contact)
│   ├── projects.html           # Full Projects Catalog
│   ├── project_detail.html     # Dedicated Project Case Study & Metadata View
│   ├── 404.html                # Branded 404 Error Page
│   └── 500.html                # Branded 500 Server Error Page
│
└── static/
    ├── css/
    │   └── style.css           # Custom Design System, CSS Variables, Typography & Animations
    ├── js/
    │   └── script.js           # Navigation, Typing Animation, Filter Tabs, Modal Loader, Contact API
    ├── images/
    │   ├── profile.jpg         # Developer photo
    │   ├── profile.svg         # High-resolution developer profile badge
    │   ├── favicon.svg         # Monogram SVG favicon
    │   ├── certificates/       # High-resolution academic & industry certificates
    │   ├── smartpos.svg        # SmartPOS POS terminal vector graphic
    │   ├── elara.svg           # ELARA AI neural core illustration
    │   ├── smartbin.svg        # Smart Bin IoT graphic
    │   └── space_dodger.svg    # Space Dodger 2D arcade graphic
    └── files/
        └── Michael_Angelo_Gertos_Resume.pdf  # Generated Resume Document
```

---

## 🚀 Getting Started Locally

### Prerequisites
- Python 3.10+ installed on your system.

### Installation & Run

1. Open your terminal in the project directory:
   ```bash
   cd "C:\Personal Digital Portfolio"
   ```

2. Install dependencies:
   ```bash
   python -m pip install -r requirements.txt
   ```

3. (Optional) Re-generate the official PDF resume:
   ```bash
   python generate_resume_pdf.py
   ```

4. Launch the Flask application:
   ```bash
   python app.py
   ```

5. Open your browser and navigate to:
   ```
   http://127.0.0.1:5000
   ```

---

## 🌐 Deploying to Vercel

This repository is pre-configured for zero-configuration serverless deployment on [Vercel](https://vercel.com):

1. **Commit and push changes to GitHub**:
   ```bash
   git add .
   git commit -m "Prepare portfolio for Vercel deployment"
   git push origin main
   ```
2. **Import repository into Vercel**:
   - Go to [vercel.com](https://vercel.com) and log in with your GitHub account.
   - Click **Add New...** → **Project**.
   - Select `personal-digital-portfolio` from your GitHub repositories.
3. **Environment Variables (Recommended)**:
   - Expand the **Environment Variables** panel in Vercel.
   - Add `SECRET_KEY` with a strong random string (e.g. `gertos-portfolio-live-2026`).
4. **Deploy**:
   - Click **Deploy**. Vercel will build the serverless Python functions and deploy your static assets to Edge CDN.
   - Your live public URL (e.g., `https://personal-digital-portfolio.vercel.app`) will be available immediately!

---

## 🔗 Available Endpoints

| Route | Method | Description |
| :--- | :--- | :--- |
| `/` | `GET` | Main Portfolio Page (all 11 sections) |
| `/projects` | `GET` | Dedicated Projects & Systems Catalog |
| `/project/<slug>` | `GET` | Standalone Case Study for a specific project |
| `/download-resume` | `GET` | Downloads `Michael_Angelo_Gertos_Resume.pdf` |
| `/api/projects` | `GET` | Returns JSON array of all projects |
| `/api/project/<slug>` | `GET` | Returns JSON details for modal rendering |
| `/api/contact` | `POST` | Validates and stores contact inquiries in SQLite |

---

## 👤 Profile & Attribution

- **Name**: Michael Angelo Gertos
- **Location**: Kalilangan, Bukidnon, Philippines
- **Email**: michaelangelogertos123@gmail.com
- **Phone**: 09067224273
- **Tagline**: *"Building technology that makes work smarter, faster, and more sustainable."*
- **Institution**: Torres Capitol College Inc. (BSIT)
