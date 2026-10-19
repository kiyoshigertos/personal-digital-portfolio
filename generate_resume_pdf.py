import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT

def create_resume():
    output_dir = os.path.join(os.path.dirname(__file__), 'static', 'files')
    os.makedirs(output_dir, exist_ok=True)
    pdf_path = os.path.join(output_dir, 'Michael_Angelo_Gertos_Resume.pdf')

    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36
    )

    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'MainTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=colors.HexColor('#0f172a'),
        alignment=TA_CENTER
    )
    
    subtitle_style = ParagraphStyle(
        'Subtitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#2563eb'),
        alignment=TA_CENTER
    )

    contact_style = ParagraphStyle(
        'ContactInfo',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor('#475569'),
        alignment=TA_CENTER
    )

    section_heading = ParagraphStyle(
        'SectionHeading',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=colors.HexColor('#0f172a'),
        spaceBefore=8,
        spaceAfter=3
    )

    item_title = ParagraphStyle(
        'ItemTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=13,
        textColor=colors.HexColor('#1e293b')
    )

    item_sub = ParagraphStyle(
        'ItemSub',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor('#2563eb')
    )

    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11.5,
        textColor=colors.HexColor('#334155')
    )

    bullet_style = ParagraphStyle(
        'Bullet',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11.5,
        textColor=colors.HexColor('#334155'),
        leftIndent=12
    )

    story = []

    # Header
    story.append(Paragraph("MICHAEL ANGELO GERTOS", title_style))
    story.append(Spacer(1, 2))
    story.append(Paragraph("JUNIOR SOFTWARE DEVELOPER &bull; IT SPECIALIST &bull; FULL-STACK DEVELOPER", subtitle_style))
    story.append(Spacer(1, 2))
    story.append(Paragraph("Kalilangan, Bukidnon, Philippines &bull; 09067224273 &bull; michaelangelogertos123@gmail.com &bull; github.com/kiyoshigertos", contact_style))
    story.append(Spacer(1, 4))
    story.append(HRFlowable(width="100%", thickness=1.2, color=colors.HexColor('#2563eb'), spaceBefore=2, spaceAfter=6))

    # Professional Summary
    story.append(Paragraph("PROFESSIONAL SUMMARY", section_heading))
    story.append(Paragraph(
        "Information Technology student and aspiring software developer with a passion for building practical technology solutions that make work easier, faster, and more sustainable. Experienced in cross-platform development with Flutter, Python systems, database design, and hands-on IT diagnostics. Proven ability to deliver real-world client systems, troubleshoot hardware/software faults, and collaborate effectively under pressure.",
        body_style
    ))
    story.append(Spacer(1, 4))

    # Technical Skills
    story.append(Paragraph("TECHNICAL SKILLS", section_heading))
    skills_data = [
        [Paragraph("<b>Programming &amp; Mobile:</b>", body_style), Paragraph("Python, Dart, Flutter Framework", body_style)],
        [Paragraph("<b>Databases:</b>", body_style), Paragraph("MySQL, Microsoft Access", body_style)],
        [Paragraph("<b>Tools &amp; Environments:</b>", body_style), Paragraph("Git, GitHub, Visual Studio Code, Antigravity, Cursor", body_style)],
        [Paragraph("<b>IT &amp; Systems:</b>", body_style), Paragraph("Networking, Hardware Troubleshooting, Software Troubleshooting, Computer Repair, Prompt Engineering", body_style)],
        [Paragraph("<b>Currently Learning:</b>", body_style), Paragraph("Advanced Flutter Architecture, Modern Application Development", body_style)]
    ]
    t = Table(skills_data, colWidths=[140, 400])
    t.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
    ]))
    story.append(t)
    story.append(Spacer(1, 4))

    # Featured Experience & Client Projects
    story.append(Paragraph("EXPERIENCE &amp; CLIENT PROJECTS", section_heading))
    
    # Freelance
    story.append(Paragraph("<b>Freelance Software Developer</b> &bull; SmartPOS Client Deployments", item_title))
    story.append(Paragraph("Client Locations: Jamelo Store, Hanmae's Store, MJMK Convenience Store", item_sub))
    story.append(Paragraph("&bull; Architected and deployed SmartPOS, a multi-device point-of-sale and inventory management system.", bullet_style))
    story.append(Paragraph("&bull; Engineered responsive interfaces supporting smartphones, tablets, and desktop computers.", bullet_style))
    story.append(Paragraph("&bull; Implemented sales tracking, product catalog indexing, and daily operational summary tools for store owners.", bullet_style))
    story.append(Spacer(1, 4))

    # Harvey's
    story.append(Paragraph("<b>Assistant Technician</b> &bull; Harvey's Electronic and Repair Shop and Services", item_title))
    story.append(Paragraph("Kalilangan, Bukidnon, Philippines | September 2023 &ndash; February 2024", item_sub))
    story.append(Paragraph("&bull; Conducted client intake interviews to diagnose device issues and identify root causes.", bullet_style))
    story.append(Paragraph("&bull; Performed hardware and software diagnostics, component servicing, and system maintenance using repair tools.", bullet_style))
    story.append(Paragraph("&bull; Successfully repaired and recovered severely virus-infected laptops and restored operating integrity.", bullet_style))
    story.append(Spacer(1, 4))

    # Featured Systems & Research
    story.append(Paragraph("FEATURED PROJECTS", section_heading))
    story.append(Paragraph("<b>ELARA AI</b> &ndash; AI Personal Assistant Project (Reverse-Psychology Branding: <i>'Don't let ELARA fool you. Let ELARA solve you.'</i>)", item_title))
    story.append(Paragraph("&bull; Implemented core conversational reasoning and structured prompt pipelines; architecting planned offline and student assistance workflows.", bullet_style))
    story.append(Paragraph("<b>Smart Bin</b> &ndash; IoT &amp; Smart Waste Management Concept", item_title))
    story.append(Paragraph("&bull; Engineered IoT waste monitoring concept aimed at automated fill-level alerts and environmental sustainability.", bullet_style))
    story.append(Paragraph("<b>Space Dodger</b> &ndash; 2D Game Project", item_title))
    story.append(Paragraph("&bull; Built arcade collision handling, player coordinate physics, and interactive game loop logic.", bullet_style))
    story.append(Spacer(1, 4))

    # Education
    story.append(Paragraph("EDUCATION &amp; LEADERSHIP", section_heading))
    story.append(Paragraph("<b>Bachelor of Science in Information Technology</b> (Pursuing: 2024 &ndash; Present)", item_title))
    story.append(Paragraph("Torres Capitol College, Inc. (formerly Philippine Countryville College) &bull; Leadership: PIO, IT Department", item_sub))
    story.append(Paragraph("&bull; <b>3x Consecutive Dean's Lister:</b> AY 24-25 1st Sem (1.42 GWA) &bull; AY 24-25 2nd Sem (1.56 GWA) &bull; AY 25-26 1st Sem (1.72 GWA)", bullet_style))
    story.append(Paragraph("&bull; <b>Academic Recognitions:</b> Latin Award Candidate, Best Programmer Award, Capstone of the Year", bullet_style))
    story.append(Paragraph("&bull; <b>Secondary Education:</b> Academic Excellence with Honors (90% Average Grade) &ndash; DepEd Kalilangan National High School", bullet_style))
    story.append(Spacer(1, 4))

    # Awards & Certifications
    story.append(Paragraph("VERIFIED CERTIFICATIONS &amp; HONORS", section_heading))
    story.append(Paragraph("&bull; <b>TESDA National Certificate II (CSS NC II):</b> Computer Systems Servicing (Cert No: 24101302001324 &bull; Valid 2024&ndash;2029)", bullet_style))
    story.append(Paragraph("&bull; <b>Dean's List Certificate of Recognition:</b> Torres Capitol College, Inc. (March 2026 &bull; 1.72 GWA)", bullet_style))
    story.append(Paragraph("&bull; <b>Dean's List Certificates:</b> Philippine Countryville College, Inc. (1.42 &amp; 1.56 GWA Distinctions)", bullet_style))
    story.append(Paragraph("&bull; <b>DICT Seminar-Workshop Certificate:</b> Digital Danger Zone &ndash; Cybersecurity &amp; Digital Defense (DICT Region 10)", bullet_style))
    story.append(Paragraph("&bull; <b>Academic Defense Certificate:</b> BSIT Gameplay Defense &ndash; Interactive Systems Presentation", bullet_style))
    story.append(Paragraph("&bull; <b>Robotics Championship &ndash; Champion (1st Place):</b> Institutional Automation Challenge (2025)", bullet_style))
    story.append(Paragraph("&bull; <b>Hackathon Championship &ndash; 1st Place:</b> Rapid Software Engineering Hackathon (2024)", bullet_style))
    story.append(Paragraph("&bull; <b>1st Place &ndash; Sayaw Arnis/Kali:</b> Cultural &amp; Martial Arts Competition (2025)", bullet_style))
    story.append(Paragraph("&bull; <b>DEVCON Bits of Light Roadshow:</b> Frontend Forge Workshop &bull; DEVCON Bukidnon &amp; DICT Region X (July 2026)", bullet_style))

    doc.build(story)
    print("Resume PDF generated successfully at:", pdf_path)

if __name__ == '__main__':
    create_resume()
