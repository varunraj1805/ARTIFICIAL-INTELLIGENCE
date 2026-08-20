# Resume Analyzer

A lightweight desktop application that reviews resumes and compares them with target job roles. It can analyze a resume with a full job description, a simple role title, or no job description at all.

The application uses a Tkinter interface and performs local, rule-based analysis. No API key is required.

## Features

- Open resumes in TXT, Markdown, PDF, or DOCX format
- Paste resume text directly into the application
- Compare a resume with a complete job description
- Analyze simple roles such as `Software Engineer` automatically
- Suggest suitable roles when no job description is provided
- Display an overall score out of 100
- Show matched skills and skills to consider
- Check resume sections such as summary, experience, education, skills, and projects
- Detect measurable achievements and provide improvement recommendations

## Requirements

- Python 3.10 or newer
- Windows, macOS, or Linux
- Tkinter, normally included with the standard Python installation

## Installation

Clone the repository and open the project folder:

```bash
git clone https://github.com/YOUR-USERNAME/YOUR-REPOSITORY.git
cd YOUR-REPOSITORY
```

Create and activate a virtual environment.

### Windows PowerShell

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### macOS or Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install the optional document readers:

```bash
python -m pip install pypdf python-docx
```

## Run the Application

From the project directory, run:

```bash
python artifical_intelligence.py
```

The main file is named `artifical_intelligence.py` to match the current project. The spelling is retained for compatibility.

## How to Use

1. Open the application.
2. Paste your resume or click **Open file**.
3. Select a TXT, Markdown, PDF, or DOCX resume.
4. Optionally enter a complete job description or a simple role such as `Software Engineer`.
5. Click **Analyze resume**.
6. Review the score, matched skills, missing skills, best-fit roles, and recommendations.

### Analysis Modes

#### With a full job description

The analyzer extracts recognized skills from the job description and compares them with the resume.

#### With a simple job role

Built-in role profiles expand titles such as:

- Software Engineer
- Software Developer
- Web Developer
- Python Developer
- Data Scientist
- Machine Learning Engineer
- AI Engineer
- Frontend Developer
- Backend Developer

#### Without a job description

The analyzer reviews the resume and recommends the strongest matching roles based on detected skills.

## Supported Skills

The built-in vocabulary includes programming, web development, cloud, data, AI, design, and workplace skills such as:

- Python, Java, JavaScript, TypeScript, C++
- SQL, HTML, CSS, React, Node.js
- Django, Flask, FastAPI, REST APIs
- AWS, Azure, Docker, Kubernetes
- Git, GitHub, Linux
- Machine Learning, Deep Learning, NLP
- Data Analysis, Data Science, Excel, Tableau, Power BI
- Agile, Scrum, Communication, Leadership, Research

The skill vocabulary and role profiles can be expanded in `artifical_intelligence.py`.

## Project Structure

```text
.
├── artifical_intelligence.py   # Resume analyzer desktop application
├── speech to text.py            # Microphone speech-to-text utility
├── style_transfer_utils.py     # Existing utility module
├── meeting_notes/               # Existing meeting note files
└── saved audio/                 # Existing saved audio files
```

## Limitations

- Analysis is rule-based and is not a substitute for a recruiter or professional career advisor.
- Only skills in the built-in vocabulary are matched automatically.
- Scanned or image-only PDFs may not contain extractable text.
- The application does not currently use semantic AI or a language model.
- A complete job description gives more accurate results than a job title alone.

## Contributing

1. Create a new branch:

```bash
git checkout -b improve-resume-analyzer
```

2. Make and test your changes.
3. Commit your changes:

```bash
git add .
git commit -m "Improve resume analyzer"
```

4. Push the branch and open a pull request on GitHub.

## License

Add a license before publishing if this project will be shared publicly. The MIT License is a common choice for small personal projects.
