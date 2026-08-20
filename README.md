# 📄 Resume Analyzer

> **A lightweight desktop AI-inspired resume analysis tool that evaluates resumes against target job roles and provides actionable improvement recommendations.**

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python" alt="Python">
  <img src="https://img.shields.io/badge/GUI-Tkinter-orange?style=for-the-badge" alt="Tkinter">
  <img src="https://img.shields.io/badge/Analysis-Rule--Based-green?style=for-the-badge" alt="Rule Based">
  <img src="https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey?style=for-the-badge" alt="Platform">
</p>

---

## 🚀 Overview

**Resume Analyzer** is a lightweight desktop application designed to help users understand how well their resume matches a desired job role.

The application can analyze a resume using:

* 🎯 A complete **Job Description**
* 💼 A simple **Job Role**
* 🔍 **No job description**, using the resume itself to suggest suitable roles

The analyzer performs **local, rule-based analysis**, so **no API key or internet connection is required** for the core analysis.

---

## ✨ Features

| Feature                         | Description                                                  |
| ------------------------------- | ------------------------------------------------------------ |
| 📂 **Multiple File Formats**    | Open TXT, Markdown, PDF, and DOCX resumes                    |
| 📝 **Direct Text Input**        | Paste resume content directly into the application           |
| 🎯 **Job Description Matching** | Compare a resume against a complete job description          |
| 💼 **Role Analysis**            | Analyze roles such as Software Engineer or AI Engineer       |
| 🤖 **Role Suggestions**         | Recommend suitable roles when no job description is provided |
| 📊 **Resume Score**             | Generate an overall score out of 100                         |
| ✅ **Skill Matching**            | Display skills detected in the resume                        |
| ⚠️ **Missing Skills**           | Identify skills that may need to be added                    |
| 📑 **Section Analysis**         | Check Summary, Experience, Education, Skills, and Projects   |
| 📈 **Achievement Detection**    | Detect measurable achievements and evidence                  |
| 💡 **Recommendations**          | Provide suggestions to improve the resume                    |

---

## 🧠 How It Works

```text
                📄 RESUME
                    │
                    ▼
          ┌─────────────────────┐
          │   Text Extraction   │
          └──────────┬──────────┘
                     │
                     ▼
          ┌─────────────────────┐
          │ Skill Identification│
          └──────────┬──────────┘
                     │
          ┌──────────┴──────────┐
          ▼                     ▼
   🎯 Job Description      💼 Job Role
          │                     │
          └──────────┬──────────┘
                     ▼
          ┌─────────────────────┐
          │ Resume Comparison   │
          └──────────┬──────────┘
                     ▼
          ┌─────────────────────┐
          │    📊 Score /100    │
          └──────────┬──────────┘
                     ▼
       ┌───────────────────────────┐
       │ Skills • Roles • Sections │
       │ Achievements • Suggestions│
       └───────────────────────────┘
```

---

## 🛠️ Technologies Used

### 💻 Core

* 🐍 **Python 3.10+**
* 🖥️ **Tkinter**
* 📄 **PyPDF**
* 📑 **python-docx**

### 🧠 Analysis

* Rule-based text analysis
* Skill matching
* Role-profile matching
* Resume section detection
* Achievement detection

---

## 📋 Requirements

Before running the project, make sure you have:

* 🐍 Python **3.10 or newer**
* 💻 Windows, macOS, or Linux
* 🖼️ Tkinter

> 💡 Tkinter is normally included with the standard Python installation.

---

## ⚙️ Installation

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/YOUR-USERNAME/YOUR-REPOSITORY.git
cd YOUR-REPOSITORY
```

### 2️⃣ Create a Virtual Environment

#### 🪟 Windows PowerShell

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

#### 🍎 macOS / 🐧 Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3️⃣ Install Dependencies

```bash
python -m pip install pypdf python-docx
```

---

## ▶️ Run the Application

Run the following command from the project directory:

```bash
python artifical_intelligence.py
```

> ⚠️ The filename `artifical_intelligence.py` intentionally retains its current spelling for compatibility with the existing project.

---

## 🖥️ How to Use

### Step 1 — 📄 Add Your Resume

Open the application and either:

* 📂 Click **Open File**
* 📝 Paste your resume text directly

Supported formats:

```text
TXT
Markdown
PDF
DOCX
```

### Step 2 — 🎯 Enter a Target

You can provide:

**Option A — Full Job Description**

Paste the complete job description.

**Option B — Job Role**

Enter a role such as:

```text
Software Engineer
```

**Option C — No Job Description**

Leave the job description field empty and let the application recommend suitable roles.

### Step 3 — 🔍 Analyze

Click:

```text
Analyze Resume
```

### Step 4 — 📊 Review Results

The application displays:

* ⭐ Overall Resume Score
* ✅ Matched Skills
* ⚠️ Skills to Consider
* 💼 Best-Fit Roles
* 📑 Resume Section Analysis
* 📈 Measurable Achievement Detection
* 💡 Improvement Recommendations

---

# 🎯 Analysis Modes

## 1. 📋 Full Job Description

When a complete job description is provided, the analyzer extracts recognized skills from the description and compares them against the resume.

```text
Resume
   +
Job Description
   ↓
Skill Extraction
   ↓
Skill Comparison
   ↓
📊 Resume Score
```

---

## 2. 💼 Simple Job Role

The application supports built-in role profiles that expand simple job titles into relevant skills.

### Supported Roles

* 👨‍💻 Software Engineer
* 💻 Software Developer
* 🌐 Web Developer
* 🐍 Python Developer
* 📊 Data Scientist
* 🤖 Machine Learning Engineer
* 🧠 AI Engineer
* 🎨 Frontend Developer
* ⚙️ Backend Developer

Example:

```text
Input:
Machine Learning Engineer

        ↓

Role Profile

Python
Machine Learning
Deep Learning
NLP
Data Analysis
        ↓

Resume Comparison
```

---

## 3. 🔎 No Job Description

If no job description is provided, the application analyzes the resume and identifies the strongest matching roles based on detected skills.

Example:

```text
Resume Skills
     ↓
Python
Machine Learning
NLP
Data Analysis
     ↓
Role Matching
     ↓
🎯 Recommended Roles
```

---

# 🧰 Supported Skills

The built-in skill vocabulary covers several technical and professional categories.

### 🐍 Programming

* Python
* Java
* JavaScript
* TypeScript
* C++

### 🌐 Web Development

* HTML
* CSS
* React
* Node.js
* Django
* Flask
* FastAPI
* REST APIs

### ☁️ Cloud & DevOps

* AWS
* Azure
* Docker
* Kubernetes

### 📊 Data & Analytics

* SQL
* Data Analysis
* Data Science
* Excel
* Tableau
* Power BI

### 🤖 Artificial Intelligence

* Machine Learning
* Deep Learning
* NLP

### 🔧 Tools & Platforms

* Git
* GitHub
* Linux

### 🤝 Professional Skills

* Agile
* Scrum
* Communication
* Leadership
* Research

> 💡 The skill vocabulary and role profiles can be expanded directly in `artifical_intelligence.py`.

---

# 📁 Project Structure

```text
Resume-Analyzer/
│
├── 📄 artifical_intelligence.py
│   └── Main Resume Analyzer application
│
├── 🎤 speech to text.py
│   └── Microphone speech-to-text utility
│
├── 🎨 style_transfer_utils.py
│   └── Existing utility module
│
├── 📂 meeting_notes/
│   └── Existing meeting note files
│
└── 🔊 saved audio/
    └── Existing saved audio files
```

---

# 📊 What the Analyzer Checks

The application evaluates several important aspects of a resume.

### 📑 Resume Sections

* ✅ Professional Summary
* ✅ Experience
* ✅ Education
* ✅ Skills
* ✅ Projects

### 🧠 Content Analysis

* 🔍 Skill detection
* 🎯 Job-role matching
* 📊 Overall score
* 📈 Measurable achievements
* ⚠️ Missing skills
* 💡 Improvement recommendations

---

# ⚠️ Limitations

Although the project provides useful automated feedback, there are some limitations:

* 🔹 Analysis is **rule-based** and is not a replacement for a recruiter or professional career advisor.
* 🔹 Only skills included in the built-in vocabulary are automatically matched.
* 🔹 Scanned or image-only PDFs may not contain extractable text.
* 🔹 The current version does **not use semantic AI or a language model**.
* 🔹 A complete job description generally provides more accurate matching than a job title alone.

---

# 🔮 Future Improvements

Possible future enhancements include:

* 🤖 Integrate an LLM for semantic resume analysis
* 🧠 Add semantic similarity using embeddings
* 📊 Add visual charts for resume scoring
* 📄 Generate an improved resume automatically
* 🎯 Add ATS compatibility scoring
* 🌐 Build a web version
* 🔗 Add LinkedIn profile analysis
* 🎤 Add voice-based resume editing
* 📈 Track resume improvements over time
* 💾 Export analysis reports as PDF
* 🧑‍💼 Add industry-specific resume recommendations

---

# 🤝 Contributing

Contributions are welcome!

### 1️⃣ Create a Branch

```bash
git checkout -b improve-resume-analyzer
```

### 2️⃣ Make Your Changes

Implement and test your improvements.

### 3️⃣ Commit

```bash
git add .
git commit -m "Improve resume analyzer"
```

### 4️⃣ Push

```bash
git push origin improve-resume-analyzer
```

Then open a **Pull Request** on GitHub.

---

# 📜 License

A license should be added before publishing the project publicly.

The **MIT License** is a common choice for small personal and academic projects.

---

# 👨‍💻 Author

**Varun Raj Nannam**

🎓 B.Tech — Artificial Intelligence & Machine Learning

💡 Interested in:

`Artificial Intelligence` • `Machine Learning` • `NLP` • `Python` • `Software Development`

---

# ⭐ Support

If you find this project useful:

⭐ **Star the repository**

🍴 **Fork the project**

🐛 **Report issues**

💡 **Suggest improvements**

🤝 **Contribute to the project**

---

<p align="center">
  <b>🚀 Resume Analyzer — Analyze Better. Improve Smarter. Get Hired.</b>
</p>
