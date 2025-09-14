from __future__ import annotations

import base64
import csv
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional

import streamlit as st
from PIL import Image

# ======================
# CONFIG & LIGHT STYLING
# ======================
st.set_page_config(
    page_title="Abhisekh Bajracharya",
    page_icon="📊",
    layout="wide"
)
def pill(text: str):
    st.markdown(f"<span style='background:#eee;padding:3px 8px;border-radius:12px;margin-right:4px'>{text}</span>", unsafe_allow_html=True)
# ----------------------
# Utility Functions
# ----------------------
def asset(file: str | Path) -> Path:
    """Return the path to an asset file"""
    return Path(__file__).parent / "assets" / file

def load_bytes(path: Path) -> bytes:
    """Read file bytes safely"""
    with open(path, "rb") as f:
        return f.read()

def resume_bytes():
    """Load resume PDF if available"""
    f = asset("Resume.pdf")
    return load_bytes(f) if f.exists() else None

def add_bg_from_local(image_file):
    """Add background image from local file"""
    with open(image_file, "rb") as f:
        data = f.read()
    encoded = base64.b64encode(data).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpg;base64,{encoded}");
            background-size: cover;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# ----------------------
# Background Image (safe)
# ----------------------
try:
    add_bg_from_local("assets/background.jpg")
except FileNotFoundError:
    st.warning("⚠️ Background image not found, continuing without it.")

# ----------------------
# CSS Styling
# ----------------------
st.markdown(
    """
    <style>
    .card {
        background-color: #0a2540; /* dark blue */
        color: white;
        padding: 20px;
        margin: 10px 0;
        border-radius: 10px;
        font-size: 16px;
        line-height: 1.5;
    }
    .card .small {
        font-size: 14px;
        color: #d0e0ff;
        display: block;
        margin-top: 8px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

def combine_images(files_and_widths, bg=(255,255,255)):
    imgs = []
    for fname, target_w in files_and_widths:
        img = Image.open(fname).convert("RGBA")
        w0,h0 = img.size
        new_h = int(h0 * (target_w / w0))
        img = img.resize((target_w, new_h), Image.LANCZOS)
        imgs.append(img)
    max_h = max(im.size[1] for im in imgs)
    padded = []
    for im in imgs:
        w,h = im.size
        if h < max_h:
            new = Image.new("RGBA", (w, max_h), (255,255,255,0))
            new.paste(im, (0, (max_h - h)//2), im)
            padded.append(new)
        else:
            padded.append(im)
    total_w = sum(im.size[0] for im in padded)
    out = Image.new("RGBA", (total_w, max_h), bg + (255,))
    x = 0
    for im in padded:
        out.paste(im, (x, 0), im)
        x += im.size[0]
    return out.convert("RGB")

def skill_bar(label: str, pct: int):
    pct = max(0, min(int(pct), 100))
    st.markdown(
        f"""
<div class='skill'>
  <div class='label'>{label}</div>
  <div class='bar'><div class='fill' style='width:{pct}%;'></div></div>
</div>
""",
        unsafe_allow_html=True,
    )

# ----------------------
# Tabs
# ----------------------
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9, tab10 = st.tabs(
    ["Home", "Resume", "Projects", "Skills", "Contact", "Interests and Hobbies", "Organizations", "Dashboard Project", "DevOps Flask Project", "Nasa Project"]
)
# === GLOBAL CONFIG ===
LINKEDIN = "https://www.linkedin.com/in/abhisekhbajracharya"
GITHUB = "https://github.com/abhisekhbajracharya"
RESUME_URL = None  # or "https://..." if hosted online
FORM_SUBMIT_EMAIL = None  # or your email if using FormSubmit

# =====================
# SIDEBAR — QUICK ACCESS + CONTACT
# =====================
st.sidebar.title("🔗 Quick Access")
st.sidebar.link_button("💼 LinkedIn", LINKEDIN)
st.sidebar.link_button("🧠 GitHub", GITHUB)


# === TAB 1: ABOUT ME ===
with tab1:
    combined = combine_images([("assets/UTA.jpg", 300), ("assets/pho1.jpg", 300), ("assets/JPM.jpg", 300)])
    st.image(combined, use_container_width=False)

    st.markdown("## 👋 Who am I?")
    st.markdown("""
    Hello, and welcome to my website. My name is **Abhisekh**.  
    I created this space to give you a clear and personal view of who I am—beyond what a résumé alone can show.  

    In today’s fast-paced hiring environment, where thousands of applications often compete for a job or internship, I believe this is the most effective way to present my background, interests, and strengths.
    """)

    st.markdown("## 💡 What do I (as a person) have to offer?")
    st.info("I recently graduated with a bachelors degree in computer science in December 2024, and am actively developing my skills in **data engineering, cloud platforms (Snowflake, Azure), and applied AI.** My current employment is at JP Morgan Chase as a Data Entry Specalist at the Lewisville, Texas.")
    st.markdown("""
    My goal is to contribute to building scalable solutions that deliver meaningful results.  
    While I am still growing my expertise, I am eager to learn quickly, apply myself to real-world projects, and contribute as a dedicated member of your team.
    """)
    with st.expander("📊 JPMorgan – Current Role"):
        from pathlib import Path
        image_path = Path(__file__).parent / "assets" / "JPM.jpg"
        if image_path.is_file():
            st.image(image_path, width=300)
        else:
            st.error(f"Image not found at {image_path}")
            st.markdown("""
            I’m currently working at JPMorgan in a datahouse environment, where I handle large volumes of information to ensure accuracy and consistency.  

        My responsibilities include:  
        - Processing and validating data  
        - Resolving discrepancies  
        - Maintaining clean records that support decision-making across teams  

        This experience has strengthened my interest in data-focused work and motivated me to deepen my technical skills.
        """)

    with st.expander("📦 Amazon (Irving, TX | June 2023 – June 2025)"):
        from pathlib import Path
        image_path = Path(__file__).parent / "assets" / "amazon.png"
        if image_path.is_file():
            st.image(image_path, width=300)
        else:
            st.error(f"Image not found at {image_path}")        
            st.markdown("""
            At the same time, I worked as an Supply chain associate at an Amazon warehouse. Balancing this with my studies—like taking a Data Mining exam and then going straight to a shift—pushed me to become disciplined and reliable.  
        Amazon offered to pay for my tuition which greatly helped me continue on my studies.
        **Key takeaways:**  
        - Hands-on experience in inventory management & workflow coordination  
        - Meeting strict performance goals  
        - Reinforced the importance of efficiency and responsibility in large-scale operations
        """)

    with st.expander("🚀 NASA L’SPACE Academy (Remote | May – Aug 2024)"):
        from pathlib import Path
        image_path = Path(__file__).parent / "assets" / "lspace.png"
        if image_path.is_file():
            st.image(image_path, width=300)
        else:
            st.error(f"Image not found at {image_path}")        
            st.markdown("""
                    In 2024, I joined **NASA’s L’SPACE Academy**, where I contributed to **mission planning and systems design** for a lunar rover project.  
                    This experience challenged me to bridge technical analysis with team collaboration, working alongside students from diverse disciplines to solve complex design problems.  
                    
                    As part of the **NASA Lunar Design – Data Analysis track**, I:  
                    - Queried **historical mission datasets in BigQuery** to uncover trends in payload efficiency and failure rates.  
                    - Built **data flow pipelines with DBT**, supporting structured testing and automated reporting.  
                    - Modeled **component performance with SQL-driven metrics**, achieving a **20% improvement in throughput analysis**.  
                    
                    Through this project, I gained hands-on exposure to **data-driven decision-making in aerospace contexts** while strengthening my skills in teamwork, communication, and systems thinking.  

                    Here is the link to the program: https://www.lspace.asu.edu/
                    """)


    with st.expander("🛍️ Retail Store Supervisor – Burkes Outlet (Irving, TX | June – August 2022)"):
        from pathlib import Path
        image_path = Path(__file__).parent / "assets" / "burkes.jpg"
        if image_path.is_file():
            st.image(image_path, width=300)
        else:
            st.error(f"Image not found at {image_path}")        
            st.markdown("""
                    In 2022, while searching for additional opportunities across Irving, I joined **Burkes Outlet** as a **Retail Store Supervisor**. The team was impressed by my initiative and drive, and I was quickly trusted with leadership responsibilities.  
                    **Key Contributions:**  
                    - Supervised **daily retail operations**, ensuring smooth workflow and compliance with company standards.  
                    - Managed **confidential personnel matters**, including timecard approvals and employee dispute resolution.  
                    - **Trained new hires** in customer service protocols, safety procedures, and workplace expectations.  
                    - Utilized **Excel for staffing logs and inventory reporting**, and managed scheduling through Word and Outlook.  
                    """)


    with st.expander("🎓 Academic Projects"):
        st.markdown("""
        That interest grew during my academic projects, where I built predictive models, designed dashboards, and developed AI-powered business insights.  

        These projects showed me how technical skills can be applied to solve practical problems, and they gave me a foundation for working with data in a meaningful way.
        """)

    st.markdown("## 🎯 Career Goals & Vision")
    st.markdown("""
    Looking ahead, I want to bring these experiences together and focus on **AI, automation, and cloud platforms like Snowflake and Azure.**  
    My goal is to keep growing my skills and contribute to projects that use data to create impactful, scalable solutions.  

    Over the next **3–5 years**, I aim to:  
    - Gain hands-on experience through IT internships and entry-level roles  
    - Strengthen my foundation in data, cloud platforms, and automation  
    - Contribute to real projects where I can learn from experienced teams  
    - Grow into roles that allow me to apply problem-solving and technical skills to make a real impact  
    """)


# === TAB 2: RESUME ===
with tab2:

    st.subheader("🏛️ Download here!")

    # --- Download Resume ---
    resume_file = asset("Resume.pdf")
    pdf_bytes = load_bytes(resume_file)

    if pdf_bytes:
        st.download_button(
            label="⬇️ Download Full Resume (PDF)",
            data=pdf_bytes,
            file_name="Resume.pdf",
            mime="application/pdf"
        )
    else:
        st.warning("Resume not found. Add it at `assets/Resume.pdf` to enable download.")

    st.header("📄 Resume & Experience")

    # --- Education ---
    st.subheader("🎓 Education")
    st.markdown(
        "🏫 **University of Texas at Arlington** — Bachelor of Science in Computer Science | December 2024"
    )
    st.markdown(
        "📚 **Courses Taken:** Algorithms & Data Structures | Probabilities & Statistics | Operating Systems | Computer Networks | Software Testing & Maintenance | Database Systems | Linux Systems | Cloud Computing | Information Security II | Microsoft Power Platforms | Azure Fundamentals | Datamining"
    )
    st.markdown("---")

    # --- Side-by-side Experience & Projects ---
    exp_col, proj_col = st.columns(2)

    # --- Professional Experience (Highlight JPMorgan) ---
    with exp_col:
        st.markdown("### 💼 Experience")
        st.markdown(
            "<div style= padding:12px; border-radius:10px'>"
            "⭐ <b>Data Entry | JPMorgan Chase (Contract by Adecco) — Lewisville, TX | June 2025 – Present</b>"
            "</div>", unsafe_allow_html=True
        )
        jpm_bullets = [
            "📌 Maintained accuracy and confidentiality while processing high volumes of financial data.",
            "📊 Prepared Excel templates and reports for analysis.",
            "⚡ Improved internal ETL workflows and documentation.",
            "⏱️ Supported fast-paced data handling workflows ensuring document accuracy."
        ]
        for b in jpm_bullets:
            st.markdown(f"- {b}")
        st.markdown("---")

        other_experience = {
            "Supply Chain Associate | Amazon — Irving, TX | June 2023 – June 2025": [
                "📦 Loaded packages and pallets correctly for safe transport.",
                "📱 Tracked package destinations using handheld scanners.",
                "🚀 Maintained workflow efficiency while meeting productivity & safety targets."
            ],
            "Intern | NASA L’Space Program | May 2024 – Aug 2024": [
                "🛰️ Tested drone payload subsystem performance.",
                "📝 Created system requirement checklists & validated integration.",
                "⚠️ Participated in risk analysis and suggested mitigations."
            ],
        }
        for title, bullets in other_experience.items():
            st.markdown(f"**{title}**")
            for b in bullets:
                st.markdown(f"- {b}")
            st.markdown("---")

    # --- Projects ---
    with proj_col:
        st.markdown("### 💻 Projects")
        projects = {
            "AI-Powered Business Risk Intelligence Dashboard – 2025": [
                "📊 Interactive fraud detection dashboard with Streamlit & scikit-learn.",
                "🤖 ML models flagged high-risk transactions; SHAP explainability.",
                "🔍 SQL-style filtering for business users."
            ],
            "Python-Based Data Insights & Automation Toolkit – 2025": [
                "🐍 Data cleaning, transformation, and exploratory analysis toolkit.",
                "📈 Automated Excel report generation with charts & summaries.",
                "💻 Command-line interface for batch processing."
            ],
            "DevOps-Enabled SaaS Task Management Platform – 2024": [
                "☁️ Cloud task app using React.js & MySQL; improved query performance ~30%.",
                "⚙️ CI/CD pipeline with GitHub Actions for testing & deployment.",
                "🔗 Ensured seamless frontend-backend integration."
            ],
            "CI/CD Pipeline for Flask Web App – 2023": [
                "🌐 Lightweight Flask app deployment.",
                "🐳 CI/CD workflow with GitHub Actions & Docker.",
                "🤝 Collaborated on pipeline improvements & peer reviews."
            ]
        }
        for proj, bullets in projects.items():
            st.markdown(f"**{proj}**")
            for b in bullets:
                st.markdown(f"- {b}")
            st.markdown("---")

    # --- Organizations ---
    st.subheader("🏛️ Organizations")
    st.markdown(
        "- 🚀 NASA L’Space Mission Concept Academy\n"
        "- 💻 UTA ACM (Association for Computing Machinery)\n"
        "- 🏆 UTA Hackathon Participant"
    )

    
# === TAB 3: FEATURED PROJECTS ===
with tab3:
    st.header("Featured Projects (Top 3)")

    def pill(text: str):
        st.markdown(
            f"<span style='background:#0a2540; color:white; padding:3px 8px; border-radius:12px; margin-right:4px;'>{text}</span>",
            unsafe_allow_html=True
        )

    projects: List[Dict] = [
        {
            "title": "AI-Powered Business Risk Intelligence Dashboard",
            "when": "2025",
            "desc": [
                "Streamlit dashboard for anomaly detection in transactions.",
                "scikit-learn models + SHAP for explainability.",
                "SQL-style filtering and exportable reports.",
            ],
            "image": asset("proj_risk_dashboard.png"),
            "repo": GITHUB,
            "demo": None,
            "stack": ["Python", "Streamlit", "scikit-learn", "pandas"],
            "tab_var": tab8,  # actual tab variable for Dashboard
            "tab_name": "Dashboard Project"
        },
        {
            "title": "DevOps CI/CD for Flask App",
            "when": "2024",
            "desc": [
                "GitHub Actions pipeline for test/build/deploy.",
                "Dockerized app; simplified releases and rollbacks.",
                "Reduced manual errors; faster iterations.",
            ],
            "image": asset("CI_CD.png"),
            "repo": GITHUB,
            "demo": None,
            "stack": ["GitHub Actions", "Docker", "Flask"],
            "tab_var": tab9,  # actual tab variable for DevOps Flask
            "tab_name": "DevOps Flask Project"
        },
        {
            "title": "NASA L’SPACE — Lunar Rover Systems Concept (Data Track)",
            "when": "2024",
            "desc": [
                "Queried historical mission data (BigQuery) for component performance.",
                "Modeled throughput metrics; organized data flow with dbt.",
                "Worked in a cross-disciplinary student team.",
            ],
            "image": "lspace.png",
            "repo": None,
            "demo": None,
            "stack": ["SQL", "BigQuery", "dbt", "Excel"],
            "tab_var": tab8,  # still Dashboard
            "tab_name": "Nasa Project"
        },
    ]

    for p in projects:
        with st.container():
            c1, c2 = st.columns([1.2, 2])
            with c1:
                if p["image"]:
                    img_bytes = load_bytes(p["image"]) if Path(p["image"]).exists() else None
                    if img_bytes:
                        st.image(img_bytes, use_container_width=True, caption=p["title"], output_format="PNG")
                    else:
                        st.markdown(f"⚡ **See this project in the '{p['tab_name']}' tab above!**")
                        st.markdown(f"➡️ Go to {p['tab_name']} Tab")
                else:
                    st.markdown(f"⚡ **See this project in the '{p['tab_name']}' tab above!**")
                    st.markdown(f"➡️ Go to {p['tab_name']} Tab")
            with c2:
                st.markdown(f"#### {p['title']}")
                st.caption(p["when"])
                for d in p["desc"]:
                    st.write("- ", d)
                st.markdown(" ")
                for s in p["stack"]:
                    pill(s)

# === TAB 4: SKILLS ===
with tab4:
    st.header("Tech Stack")
    left, right = st.columns(2)
    with left:
        st.subheader("Core")
        skill_bar("Python", 90)
        skill_bar("SQL", 80)
        skill_bar("Streamlit", 90)
        skill_bar("scikit-learn", 75)
        skill_bar("GitHub Actions", 75)
        skill_bar("Docker", 60)
    with right:
        st.subheader("Cloud / Tools")
        skill_bar("Azure", 60)
        skill_bar("AWS", 55)
        skill_bar("Power BI", 55)
        skill_bar("Jupyter", 90)
        skill_bar("Linux", 65)

    st.caption("*Levels are honest self-assessments for quick scanning; details on request.*")
    st.markdown("### 🛠️ Skills (Levels)")

    # Skill details dictionary
    skill_details = {
        "Python": "Daily use in AI dashboards, data pipelines, and automation scripts; strong command of pandas, numpy, scikit-learn, matplotlib; end-to-end pipeline experience.",
        "SQL": "Regularly writing queries for analytics and reporting; confident in data extraction, filtering, aggregation, and joins.",
        "HTML/CSS": "Built dashboards and web interfaces; solid understanding of structuring pages and styling for clear, functional design.",
        "scikit-learn": "Applied in multiple ML projects for predictive modeling, anomaly detection, feature engineering, and pipelines.",
        "TensorFlow": "Developed neural network models; practical experience building, training, and evaluating deep learning models.",
        "GitHub Actions": "Created CI/CD pipelines for automated testing, building, and deploying apps; strong workflow experience.",
        "Docker": "Containerized applications for consistent development, testing, and deployment; experienced with images and commands.",
        "Heroku": "Deployed apps quickly; practiced in managing apps, updates, and integrations with CI/CD pipelines.",
        "AWS": "Hands-on with S3, Lambda, EC2; experienced in practical deployment and integration into projects.",
        "Azure": "Used core services for cloud-based project deployments; confident in managing storage, functions, and ML workloads.",
        "Streamlit": "Built multiple dashboards and interactive apps; highly comfortable creating polished, user-friendly interfaces.",
        "Jupyter": "Daily environment for notebooks, experimentation, and sharing data projects; central to workflow.",
        "Power BI": "Created interactive reports and dashboards; skilled in visualizing data and generating actionable insights."
    }

    # Layout: 3 columns for skills + descriptions
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f"**Python** 🟩🟩🟩🟩🟩  - {skill_details['Python']}")
        st.markdown(f"**SQL** 🟩🟩🟩🟩⬜  - {skill_details['SQL']}")
        st.markdown(f"**HTML/CSS** 🟩🟩🟩⬜⬜  - {skill_details['HTML/CSS']}")
    with col2:
        st.markdown(f"**scikit-learn** 🟩🟩🟩🟩⬜  - {skill_details['scikit-learn']}")
        st.markdown(f"**TensorFlow** 🟩🟩🟩⬜⬜  - {skill_details['TensorFlow']}")
    with col3:
        st.markdown(f"**GitHub Actions** 🟩🟩🟩🟩⬜  - {skill_details['GitHub Actions']}")
        st.markdown(f"**Docker** 🟩🟩🟩⬜⬜  - {skill_details['Docker']}")
        st.markdown(f"**Heroku** 🟩🟩🟩⬜⬜  - {skill_details['Heroku']}")

    st.markdown("### ☁️ Cloud")
    cloud1, cloud2 = st.columns(2)
    with cloud1:
        st.markdown(f"**AWS** 🟩🟩🟩⬜⬜  - {skill_details['AWS']}")
    with cloud2:
        st.markdown(f"**Azure** 🟩🟩🟩⬜⬜  - {skill_details['Azure']}")

    st.markdown("### 🧰 Tools")
    t1, t2, t3 = st.columns(3)
    with t1:
        st.markdown(f"**Streamlit** 🟩🟩🟩🟩🟩  - {skill_details['Streamlit']}")
    with t2:
        st.markdown(f"**Jupyter** 🟩🟩🟩🟩🟩  - {skill_details['Jupyter']}")
    with t3:
        st.markdown(f"**Power BI** 🟩🟩🟩⬜⬜  - {skill_details['Power BI']}")
        
    st.markdown("### 📜 Certifications")
    st.markdown("""
                **🚧 In Progress**
- 🎯 Google Data Analytics Certificate – Coursera  
- ☁️ Microsoft Azure Fundamentals (AZ-900)  

**✅ Completed**
- 🚀 NASA L'SPACE Mission Concept Academy *(Aug 2024)*  
- 🤖 *Career Essentials in Generative AI* – Microsoft & LinkedIn  
   &nbsp;&nbsp;• Foundations of generative AI  
   &nbsp;&nbsp;• Business applications  
   &nbsp;&nbsp;• Ethics  
- ✍️ *Introduction to Prompt Engineering for Generative AI*  
   &nbsp;&nbsp;• Strategies for effective AI prompts  
- 🎬 *AI and Generative AI for Video Content Creation*  
   &nbsp;&nbsp;• AI-driven video and media workflows  
- 📊 *Introduction to AI Foundations: Machine Learning*  
   &nbsp;&nbsp;• Supervised/unsupervised learning  
   &nbsp;&nbsp;• Algorithms  
   &nbsp;&nbsp;• ML lifecycle  
- 🔎 *Getting Started with AI and Machine Learning*  
   &nbsp;&nbsp;• Overview of applications  
   &nbsp;&nbsp;• Accountability  
   &nbsp;&nbsp;• Security considerations  
                """)


# === TAB 5: CONTACT ===
with tab5:
    st.header("📬 Contact")

    st.markdown("""
<style>
.contact-card {
    padding: 20px;
    border-radius: 15px;
    background: rgba(255, 255, 255, 0.05); /* subtle glass effect */
    border: 1px solid rgba(255, 255, 255, 0.2);
    box-shadow: 0 4px 15px rgba(0,0,0,0.4);
    color: #ffffff; /* make text white */
    font-size: 16px;
}
.contact-card h4 {
    margin-top: 10px;
    color: #f1c40f; /* accent color (gold/yellow) */
}
.contact-links a {
    text-decoration: none;
    margin-right: 20px;
    font-size: 22px;
    color: #1abc9c; /* teal accent for links */
}
.contact-links a:hover {
    color: #f39c12; /* hover color (orange/gold) */
}
</style>

<div class="contact-card">

**📧 Email**  
- ✉️ Personal: bajrasekh@gmail.com  
- 💼 Work: abhisekhbajracharya1@gmail.com

**🌐 Connect**  
<div class="contact-links">
    <a href="https://www.linkedin.com/in/abhisekhbajracharya" target="_blank">🔗 LinkedIn</a>
    <a href="https://github.com/" target="_blank">🐙 GitHub</a>
</div>

**📍 Location & Work Preference**  
- 🏙️ Based in Dallas–Fort Worth Metroplex, TX  
- 🌐 Open to Remote Opportunities  
- ✈️ Open to Travel as Needed  
                

**⚡ Availability**  
- ✅ Open to work  
- 🕒 Best time: Mornings & Weekends  

</div>
""", unsafe_allow_html=True)


# === TAB 6: Interests and Hobbies ===
with tab6:
    st.header("🌟 Interests and Hobbies")
    st.markdown("### 🤝 Open Source & Community")
    st.write("- Contributed to **Awesome-Data-Science** repo (docs & examples)")
    st.write("- Participated in hackathons (e.g., **HackTX**) & local meetups")
    st.write("- Volunteer mentor for Python & data analysis beginners")

    st.markdown("### 🧠 Soft Skills & Work Style")
    st.write("- Communication, teamwork, adaptability")
    st.write("- Managed deadlines in fast-paced environments")
    st.write("- Continuous learning & open feedback")

    st.markdown("### 📓 Blog & Insights")
    st.write("[How I Built My First Streamlit Dashboard](#)")
    st.write("[Trends in AI and Ethics](#)")
    st.write("[Balancing Productivity and Wellness](#)")

    st.markdown("### 📓 Poems and Short Stories")
    st.link_button("Laurel Crown of Florence", "https://docs.google.com/document/d/15pfmXz-BYTDSDe-V5B9CbuCWdeTqrRJCI1CoCDOGaDY/edit?usp=sharing")
    st.link_button("Castella", "https://docs.google.com/document/d/12HoqldBM9bv2NIVOw_jRA0y0VAnge6_-TXn_laL6o70/edit?usp=sharing")
    st.link_button("Seaheart", "")
    st.link_button("Value of Life", "https://docs.google.com/document/d/1Gh0EPCR3JYS2o9NR2GwQyYXgnwSFOuEJvMwgQN-6mWU/edit?usp=sharing")
    st.image("Seaheart_cover.png", caption="Seaheart cover", width=300)

st.subheader("🌍 My Travel Timeline")

with st.expander("✈️ 2022 Summer – Cozumel, Mexico"):
    st.write("Relaxed on white-sand beaches, explored cenotes, and practiced slow travel.")

with st.expander("🌲 2022 Fall – Broken Bow, Oklahoma"):
    st.write("Cabin retreat with friends — hiking and kayaking sparked my interest in nature photography.")

with st.expander("🏙️ 2023 Summer – Manhattan, New York"):
    st.write("Solo trip exploring tech culture, museums, and reflecting on personal goals.")

with st.expander("🌧️ 2023 Fall – Cancun, Mexico"):
    st.write("Balanced city life with nature escapes — from local parks to cultural landmarks.")

with st.expander("☀️ 2024 Summer – Rockwall, Texas"):
    st.write("Discovered local scenery, enjoyed lakeside views, and took short day hikes.")

with st.expander("🌧️ 2024 Fall – Seattle, Washington"):
    st.write("Blended tech and nature — Pike Place to lush nearby trails.")

with st.expander("🕉️ 2025 Summer – Kathmandu, Nepal"):
    st.write("Reconnected with family and heritage, visited temples, and explored historic sites.")

with st.expander("🏔️ 2025 Fall – Vail, Colorado"):
    st.write("Mountain retreat — fresh air, hiking, and deep relaxation.")


# === TAB 7: ORGANIZATIONS ===
with tab7:
    st.header("🏛️ Organizations & Communities")
    st.markdown(
        '<div class="card">🚀 <b>NASA L’SPACE Mission Concept Academy</b><br>'
        'Participated in mission design and systems analysis with a cross-disciplinary team.</div>',
        unsafe_allow_html=True
    )
    st.markdown(
        '<div class="card">💻 <b>UTA ACM</b><br>'
        'Engaged in workshops and networking to strengthen programming skills.</div>',
        unsafe_allow_html=True
    )
    st.markdown(
        '<div class="card">🏆 <b>UTA Hackathon</b><br>'
        'Collaborated on rapid prototyping and problem-solving challenges.</div>',
        unsafe_allow_html=True
    )
    st.markdown(
        '<div class="card">🌐 <b>Nepali Young Professionals</b><br>'
        'Joined networking events and mentorship discussions with peers in the U.S.</div>',
        unsafe_allow_html=True
    )
    st.markdown(
        '<div class="card">🦁 <b>Dallas Lions Club</b><br>'
        'Volunteered at community outreach and charity events.</div>',
        unsafe_allow_html=True
    )
    st.markdown(
        '<div class="card">🏮 <b>United Newa Community</b><br>'
        'Attended cultural gatherings and supported community events.</div>',
        unsafe_allow_html=True
    )

# === TAB 8: DASHBOARD PROJECT ===
with tab8:
    st.header("📊 AI-Powered Business Risk Intelligence Dashboard (2025)")
    st.write("Upload a dataset or use the sample to run anomaly detection.")

    import pandas as pd
    import numpy as np
    from sklearn.ensemble import IsolationForest
    from sklearn.neighbors import LocalOutlierFactor

    uploaded_file = st.file_uploader("Upload CSV", type="csv")
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
    else:
        rng = np.random.RandomState(42)
        df = pd.DataFrame({
            "transaction_amount": rng.normal(100, 20, 200),
            "transaction_time": rng.randint(0, 24, 200),
            "merchant_id": rng.randint(1, 50, 200)
        })

    st.subheader("Dataset Preview")
    st.dataframe(df.head())

    model_choice = st.selectbox("Choose Model", ["Isolation Forest", "Local Outlier Factor"])

    if model_choice == "Isolation Forest":
        model = IsolationForest(contamination=0.05, random_state=42)
        preds = model.fit_predict(df.select_dtypes(include=[np.number]))
    else:
        model = LocalOutlierFactor(n_neighbors=20, contamination=0.05)
        preds = model.fit_predict(df.select_dtypes(include=[np.number]))

    df["Anomaly"] = np.where(preds == -1, "Yes", "No")

    st.subheader("Anomaly Detection Results")
    st.dataframe(df)

    # Optional: safe SHAP import
    try:
        import shap
        import matplotlib.pyplot as plt
        if model_choice == "Isolation Forest":
            st.subheader("Model Explainability (SHAP)")
            explainer = shap.Explainer(model, df.select_dtypes(include=[np.number]))
            shap_values = explainer(df.select_dtypes(include=[np.number]))
            fig, ax = plt.subplots()
            shap.summary_plot(shap_values, df.select_dtypes(include=[np.number]), show=False)
            st.pyplot(fig)
    except ModuleNotFoundError:
        st.info("Install matplotlib + shap to enable explainability.")

    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("⬇ Download Results", data=csv, file_name="anomaly_results.csv", mime="text/csv")

#DEV OPS PROJECT!!!
with tab9:
    st.header("DevOps CI/CD for Flask App (2024)")

    # --- Tech stack ---
    st.markdown("**Tech Stack:**")
    for tech in ["GitHub Actions", "Docker", "Flask", "Python"]:
        pill(tech)

    # --- Flask API Simulation ---
    st.subheader("Flask API Simulation")
    endpoint = st.selectbox("Choose endpoint", ["/hello", "/predict"])
    
    if endpoint == "/predict":
        user_input = st.number_input("Input a number for prediction", min_value=0, max_value=100, value=42)
    
    if st.button("Call Endpoint"):
        if endpoint == "/hello":
            st.success("Hello, world! 🌎 Flask app response.")
        else:
            # Simple dynamic mock prediction
            pred = user_input * 2 + 3
            st.json({"input": user_input, "prediction": pred})

    # --- CI/CD Pipeline Simulation ---
    st.subheader("CI/CD Pipeline")
    pipeline_steps = [
        "Code Commit", "Lint Code", "Run Unit Tests", 
        "Build Docker Image", "Push Docker Image", 
        "Deploy to Staging", "Smoke Tests", "Deploy to Production"
    ]

    if st.button("Run CI/CD Pipeline"):
        import time
        placeholder = st.empty()
        progress = st.progress(0)
        for i, step in enumerate(pipeline_steps):
            color = "✅" if step != "Run Unit Tests" else "⚠️"  # simulate warning
            placeholder.markdown(f"{step} {color}")
            progress.progress(int((i+1)/len(pipeline_steps)*100))
            time.sleep(0.7)
        st.success("CI/CD pipeline finished!")

    # --- Deployment Dashboard ---
    st.subheader("Deployment Status")
    for env in ["Staging", "Production"]:
        st.markdown(f"**{env}:** Running ✅")

    # --- Metrics ---
    st.subheader("Mock Metrics")
    import pandas as pd, numpy as np
    df_metrics = pd.DataFrame({
        "Time": pd.date_range("2025-09-14 10:00", periods=10, freq="H"),
        "Requests Served": np.random.randint(50, 200, 10),
        "Response Time (ms)": np.random.randint(80, 300, 10)
    })
    st.line_chart(df_metrics.set_index("Time"))

with tab10:
    st.header("NASA L’SPACE — Lunar Rover Systems Concept (Data Track) (2024)")

    # Project description
    project = {
        "title": "NASA L’SPACE — Lunar Rover Systems Concept (Data Track)",
        "when": "2024",
        "desc": [
            "Queried historical mission data (BigQuery) for component performance.",
            "Modeled throughput metrics; organized data flow with dbt.",
            "Worked in a cross-disciplinary student team.",
        ],
        "stack": ["SQL", "BigQuery", "dbt", "Excel"],
    }

    def pill(text: str):
        st.markdown(
            f"<span style='background:#0a2540; color:white; padding:3px 8px; border-radius:12px; margin-right:4px;'>{text}</span>",
            unsafe_allow_html=True
        )

    # Display project info
    st.markdown(f"#### {project['title']}")
    st.caption(project["when"])
    for d in project["desc"]:
        st.write("- ", d)
    st.markdown(" ")
    for s in project["stack"]:
        pill(s)

    st.markdown("---")
    st.subheader("Simulated Data Analysis")

    import pandas as pd
    import numpy as np
    import altair as alt

    # Simulate historical mission component data
    np.random.seed(42)
    components = ["Drill", "Wheel", "Camera", "Sensor", "Arm"]
    missions = [f"Mission {i}" for i in range(1, 21)]
    df = pd.DataFrame({
        "Mission": np.random.choice(missions, 100),
        "Component": np.random.choice(components, 100),
        "Performance_Score": np.random.normal(80, 10, 100),
        "Failure_Rate": np.random.uniform(0, 0.2, 100)
    })

    st.write("Sample of mission data:")
    st.dataframe(df.head())

    # Aggregate metrics
    metrics = df.groupby("Component").agg({
        "Performance_Score": "mean",
        "Failure_Rate": "mean"
    }).reset_index()

    st.subheader("Component Performance Metrics")
    st.dataframe(metrics)

    # Chart for performance
    perf_chart = alt.Chart(metrics).mark_bar(color="#0a2540").encode(
        x=alt.X("Component", sort=None),
        y="Performance_Score",
        tooltip=["Component", "Performance_Score"]
    ).properties(title="Average Component Performance")
    st.altair_chart(perf_chart, use_container_width=True)

    # Chart for failure rate
    fail_chart = alt.Chart(metrics).mark_line(point=True, color="#ff6600").encode(
        x="Component",
        y="Failure_Rate",
        tooltip=["Component", "Failure_Rate"]
    ).properties(title="Average Component Failure Rate")
    st.altair_chart(fail_chart, use_container_width=True)

    st.markdown("---")
    st.subheader("Download Simulated Dataset")
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("⬇️ Download Mission Definition Review (MDR)", data=csv, file_name="MDR.pdf", mime="text/pdf")






