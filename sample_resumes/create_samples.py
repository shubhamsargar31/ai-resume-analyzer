"""
Utility script to generate strictly anonymized sample resumes in PDF and DOCX formats.
Used for academic evaluation and system testing.
Contains ZERO personal identifiable information (PII), protected demographic attributes, or real contact data.
"""

import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

import docx
from docx.shared import Pt, RGBColor

OUTPUT_DIR = os.path.dirname(__file__)


def create_pdf_resume(filename: str, title: str, name: str, email: str, github: str, sections_data: dict):
    filepath = os.path.join(OUTPUT_DIR, filename)
    doc = SimpleDocTemplate(filepath, pagesize=letter, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
    styles = getSampleStyleSheet()

    header_style = ParagraphStyle(
        "ResumeHeader",
        parent=styles["Heading1"],
        fontName="Helvetica-Bold",
        fontSize=18,
        leading=22,
        textColor=colors.HexColor("#1E3A8A"),
        spaceAfter=2
    )

    contact_style = ParagraphStyle(
        "ContactInfo",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9,
        leading=13,
        textColor=colors.HexColor("#4B5563"),
        spaceAfter=8
    )

    sec_title_style = ParagraphStyle(
        "SecTitle",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=11,
        leading=15,
        textColor=colors.HexColor("#1E3A8A"),
        spaceBefore=8,
        spaceAfter=3
    )

    body_style = ParagraphStyle(
        "Body",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9,
        leading=13,
        textColor=colors.HexColor("#1F2937"),
        spaceAfter=3
    )

    elements = []
    elements.append(Paragraph(name, header_style))
    elements.append(Paragraph(f"<b>{title}</b> &nbsp;|&nbsp; {email} &nbsp;|&nbsp; {github}", contact_style))
    elements.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#CBD5E1"), spaceAfter=6))

    for sec_name, content in sections_data.items():
        elements.append(Paragraph(sec_name.upper(), sec_title_style))
        if isinstance(content, list):
            for item in content:
                elements.append(Paragraph(f"• {item}", body_style))
        else:
            elements.append(Paragraph(content, body_style))
        elements.append(Spacer(1, 4))

    doc.build(elements)
    print(f"Created PDF resume: {filepath}")


def create_docx_resume(filename: str, title: str, name: str, email: str, github: str, sections_data: dict):
    filepath = os.path.join(OUTPUT_DIR, filename)
    doc = docx.Document()

    # Title & Contact
    doc.add_heading(name, level=1)
    p_sub = doc.add_paragraph(f"{title} | {email} | {github}")
    p_sub.style.font.size = Pt(9)
    p_sub.style.font.color.rgb = RGBColor(100, 100, 100)

    for sec_name, content in sections_data.items():
        doc.add_heading(sec_name.upper(), level=2)
        if isinstance(content, list):
            for item in content:
                doc.add_paragraph(item, style='List Bullet')
        else:
            doc.add_paragraph(content)

    doc.save(filepath)
    print(f"Created DOCX resume: {filepath}")


def generate_all_samples():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # 1. Data Scientist Resume (PDF)
    create_pdf_resume(
        filename="sample_data_scientist.pdf",
        title="Candidate Profile - Data Science",
        name="Sample Candidate A (Data Scientist)",
        email="candidate.datascience@sample.local",
        github="github.com/sample-portfolio-ds",
        sections_data={
            "Professional Summary": (
                "Data Scientist with 3 years of hands-on experience developing statistical machine learning models, "
                "data pipelines, and business intelligence dashboards. Proficient in Python, SQL, Pandas, NumPy, "
                "Scikit-Learn, Statistics & Probability, and Data Visualization."
            ),
            "Technical Skills": [
                "Programming Languages: Python, SQL",
                "Data Science & AI: Pandas, NumPy, Scikit-Learn, Statistics & Probability, Data Visualization",
                "Visualization & Tools: Plotly, Matplotlib, Git, Linux",
                "Secondary Competencies: TensorFlow, Docker, REST API"
            ],
            "Work Experience": [
                "Associate Data Scientist | Apex Data Systems (2022 - Present)",
                "Engineered churn prediction models using Scikit-Learn achieving 87% accuracy.",
                "Constructed automated data cleaning and aggregation pipelines in Pandas and SQL processing 2M+ records daily.",
                "Collaborated with cross-functional stakeholders to deliver interactive Plotly executive dashboards."
            ],
            "Education": [
                "Bachelor of Technology in Computer Science and Engineering | State Technical University (2018 - 2022)",
                "Relevant Coursework: Machine Learning, Statistical Methods, Database Systems, Data Structures"
            ],
            "Key Projects": [
                "Customer Segmentation Pipeline | Python, Pandas, Scikit-Learn, Plotly",
                "Designed an unsupervised clustering system using K-Means and PCA to group 50,000+ retail customers.",
                "Financial Fraud Detection Engine | Python, Scikit-Learn, SQL",
                "Developed classification model addressing class imbalance via SMOTE, reducing false positives by 22%."
            ]
        }
    )

    # 2. Full Stack Developer Resume (PDF)
    create_pdf_resume(
        filename="sample_full_stack_dev.pdf",
        title="Candidate Profile - Full Stack Engineering",
        name="Sample Candidate B (Full Stack Developer)",
        email="candidate.fullstack@sample.local",
        github="github.com/sample-portfolio-fs",
        sections_data={
            "Professional Summary": (
                "Full Stack Developer with 4 years of experience building modern web architectures. "
                "Strong background in JavaScript, TypeScript, React, Node.js, Express.js, HTML/CSS, SQL, and Git."
            ),
            "Technical Skills": [
                "Frontend: React, Next.js, TypeScript, JavaScript, HTML/CSS, Tailwind CSS",
                "Backend: Node.js, Express.js, REST API, GraphQL",
                "Databases: PostgreSQL, MongoDB, SQL, Redis",
                "DevOps & Tools: Docker, Git, CI/CD, Unit Testing"
            ],
            "Work Experience": [
                "Full Stack Engineer | Nexus Web Labs (2021 - Present)",
                "Architected high-throughput REST APIs in Node.js and Express.js supporting 100K daily active users.",
                "Built modular client components in React and TypeScript with responsive Tailwind CSS design.",
                "Optimized PostgreSQL queries and database indexes, reducing query latency by 40%."
            ],
            "Education": [
                "Bachelor of Science in Computer Science | Metropolitan Institute of Technology (2017 - 2021)"
            ],
            "Key Projects": [
                "E-Commerce SaaS Platform | React, Node.js, PostgreSQL, Docker",
                "Implemented secure payment processing, shopping cart state management, and real-time inventory updates.",
                "Team Task Manager | TypeScript, Next.js, MongoDB, Tailwind CSS",
                "Built Kanban workflow tool with drag-and-drop interactivity and WebSocket live synchronization."
            ]
        }
    )

    # 3. DevOps Engineer Resume (PDF)
    create_pdf_resume(
        filename="sample_devops_engineer.pdf",
        title="Candidate Profile - Cloud & DevOps",
        name="Sample Candidate C (DevOps Engineer)",
        email="candidate.devops@sample.local",
        github="github.com/sample-portfolio-devops",
        sections_data={
            "Professional Summary": (
                "DevOps Engineer specializing in container orchestration, cloud infrastructure, and continuous integration. "
                "Hands-on expertise with Docker, Kubernetes, AWS, Terraform, Linux, and CI/CD automation."
            ),
            "Technical Skills": [
                "Cloud & Containers: Docker, Kubernetes, AWS, Terraform",
                "Automation: CI/CD, GitHub Actions, Jenkins, Linux, Bash",
                "Languages & Tools: Python, Go, Git, Cybersecurity",
                "Networking: Network Protocols, TCP/IP, Nginx"
            ],
            "Work Experience": [
                "DevOps Engineer | CloudOps Infrastructure Corp (2022 - Present)",
                "Provisioned multi-region AWS cloud infrastructure using Terraform Infrastructure as Code (IaC).",
                "Orchestrated microservices workloads across 5 production Kubernetes clusters with zero-downtime rolling updates.",
                "Built automated CI/CD deployment pipelines cutting release cycle from 2 weeks to 2 hours."
            ],
            "Education": [
                "Bachelor of Technology in Information Technology | National Technical Academy (2018 - 2022)"
            ],
            "Key Projects": [
                "Kubernetes Cluster Automation | Terraform, Kubernetes, AWS",
                "Automated end-to-end cloud provisioning and cluster autoscaling under variable load spikes.",
                "Secure CI/CD Pipeline | Docker, GitHub Actions, Linux",
                "Engineered security scanning and container vulnerability detection into automated pull request checks."
            ]
        }
    )

    # 4. Frontend Developer Resume (DOCX)
    create_docx_resume(
        filename="sample_frontend_developer.docx",
        title="Candidate Profile - Frontend Development",
        name="Sample Candidate D (Frontend Developer)",
        email="candidate.frontend@sample.local",
        github="github.com/sample-portfolio-fe",
        sections_data={
            "Professional Summary": (
                "Frontend Web Developer with 2 years of experience crafting accessible, responsive user interfaces. "
                "Proficient in JavaScript, TypeScript, React, HTML/CSS, Tailwind CSS, and Git."
            ),
            "Technical Skills": [
                "Core Web: JavaScript, TypeScript, HTML/CSS, Tailwind CSS",
                "Frameworks: React, Next.js, Redux",
                "Tooling: Git, REST API, Unit Testing, Jest, Figma"
            ],
            "Work Experience": [
                "Frontend Developer | PixelCraft UI Studio (2023 - Present)",
                "Developed 20+ responsive web pages and reusable UI components in React and Tailwind CSS.",
                "Integrated REST API endpoints and optimized page load speed, improving Core Web Vitals by 30%.",
                "Collaborated with UX designers to convert Figma wireframes into pixel-perfect accessible interfaces."
            ],
            "Education": [
                "Bachelor of Computer Applications (BCA) | City Polytechnic College (2020 - 2023)"
            ],
            "Projects": [
                "Interactive Analytics Dashboard: Built with React, Tailwind CSS, and Chart.js.",
                "Modern Blogging Platform: Developed with Next.js, React, and Markdown integration."
            ]
        }
    )

    # 5. Data Analyst Resume (DOCX)
    create_docx_resume(
        filename="sample_data_analyst.docx",
        title="Candidate Profile - Data & Analytics",
        name="Sample Candidate E (Data Analyst)",
        email="candidate.dataanalyst@sample.local",
        github="github.com/sample-portfolio-da",
        sections_data={
            "Professional Summary": (
                "Data Analyst with 2 years of experience querying enterprise databases, automating reports, "
                "and deriving business insights. Strong expertise in SQL, Python, Pandas, and Data Visualization."
            ),
            "Technical Skills": [
                "Data Analysis: SQL, Python, Pandas, NumPy, Statistics & Probability",
                "BI & Visualization: Data Visualization, Plotly, Tableau, Power BI",
                "Databases: MySQL, PostgreSQL",
                "Workflow: Git, Agile / Scrum"
            ],
            "Work Experience": [
                "Junior Data Analyst | Metrics Analytics Inc (2023 - Present)",
                "Wrote complex SQL queries, window functions, and joins across 10M+ transaction rows.",
                "Automated weekly sales performance reporting in Python and Pandas, saving 10 team hours per week.",
                "Designed executive dashboards tracking regional KPIs, conversion rates, and retention."
            ],
            "Education": [
                "Bachelor of Science in Statistics and Mathematics | State Science College (2019 - 2023)"
            ],
            "Projects": [
                "E-Commerce Sales Insights Dashboard: SQL, Python, Pandas, and Plotly visualization.",
                "Customer Retention Cohort Analysis: Conducted cohort analysis to identify customer churn triggers."
            ]
        }
    )


if __name__ == "__main__":
    generate_all_samples()
