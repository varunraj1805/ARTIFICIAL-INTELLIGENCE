import re
import tkinter as tk
from importlib import import_module
from pathlib import Path
from tkinter import filedialog, messagebox, ttk


COMMON_SKILLS = {
	"python", "java", "javascript", "typescript", "c++", "sql", "html", "css",
	"react", "node.js", "django", "flask", "fastapi", "aws", "azure", "docker",
	"kubernetes", "git", "github", "linux", "excel", "tableau", "power bi",
	"machine learning", "deep learning", "nlp", "data analysis", "data science",
	"statistics",
	"project management", "agile", "scrum", "communication", "leadership", "research",
	"customer service", "marketing", "sales", "figma", "rest api", "mongodb", "postgresql",
}

ROLE_SKILLS = {
	"software engineer": {"python", "java", "javascript", "sql", "git", "github", "rest api", "docker"},
	"software developer": {"python", "java", "javascript", "sql", "git", "github", "rest api"},
	"web developer": {"html", "css", "javascript", "react", "node.js", "git", "rest api"},
	"python developer": {"python", "sql", "git", "github", "django", "flask", "rest api"},
	"data scientist": {"python", "sql", "machine learning", "data science", "data analysis", "statistics"},
	"machine learning engineer": {"python", "machine learning", "deep learning", "nlp", "sql", "docker"},
	"ai engineer": {"python", "machine learning", "deep learning", "nlp", "data science", "docker"},
	"frontend developer": {"html", "css", "javascript", "typescript", "react", "git"},
	"backend developer": {"python", "java", "sql", "node.js", "rest api", "docker", "git"},
}

ROLE_DESCRIPTIONS = {
	"AI Engineer": "Python, machine learning, deep learning, NLP, and data science",
	"Machine Learning Engineer": "Python, machine learning, deep learning, NLP, SQL, and Docker",
	"Python Developer": "Python, SQL, Git, Django or Flask, and REST APIs",
	"Data Scientist": "Python, SQL, machine learning, data science, data analysis, and statistics",
	"Software Engineer": "Python or Java, JavaScript, SQL, Git, REST APIs, and Docker",
	"Web Developer": "HTML, CSS, JavaScript, React, Node.js, Git, and REST APIs",
}

SECTION_NAMES = {
	"summary": ("summary", "profile", "objective", "about me"),
	"experience": ("experience", "employment", "work history", "professional experience"),
	"education": ("education", "academic background"),
	"skills": ("skills", "technical skills", "core competencies", "technologies"),
	"projects": ("projects", "selected projects", "portfolio"),
}


def extract_text(file_path):
	path = Path(file_path)
	if path.suffix.lower() in {".txt", ".md"}:
		return path.read_text(encoding="utf-8", errors="ignore")
	if path.suffix.lower() == ".pdf":
		try:
			PdfReader = import_module("pypdf").PdfReader
		except ImportError as error:
			raise RuntimeError("PDF support needs pypdf. Install it with: pip install pypdf") from error
		return "\n".join(page.extract_text() or "" for page in PdfReader(path).pages)
	if path.suffix.lower() == ".docx":
		try:
			Document = import_module("docx").Document
		except ImportError as error:
			raise RuntimeError("DOCX support needs python-docx. Install it with: pip install python-docx") from error
		return "\n".join(paragraph.text for paragraph in Document(path).paragraphs)
	raise RuntimeError("Choose a .txt, .md, .pdf, or .docx resume file.")


def find_skills(text):
	normalized = text.lower()
	return sorted(skill for skill in COMMON_SKILLS if re.search(r"(?<!\w)" + re.escape(skill) + r"(?!\w)", normalized))


def find_target_skills(job_description):
	job_lower = job_description.lower().strip()
	target_skills = set(find_skills(job_description))
	for role, skills in ROLE_SKILLS.items():
		if re.search(r"(?<!\w)" + re.escape(role) + r"(?!\w)", job_lower):
			target_skills.update(skills)
	return target_skills


def suggest_roles(resume):
	resume_skills = set(find_skills(resume))
	role_scores = []
	for role_name, description in ROLE_DESCRIPTIONS.items():
		role_key = role_name.lower()
		role_skills = ROLE_SKILLS.get(role_key, set())
		if role_name == "Data Scientist":
			role_skills = {"python", "sql", "machine learning", "data science", "data analysis", "statistics"}
		matched = resume_skills & role_skills
		score = round(len(matched) / len(role_skills) * 100)
		role_scores.append((score, role_name, matched, description))
	return sorted(role_scores, reverse=True)


def analyze_resume(resume, job_description):
	resume_lower = resume.lower()
	resume_skills = set(find_skills(resume))
	job_skills = find_target_skills(job_description)
	suggested_roles = suggest_roles(resume) if not job_description.strip() else []
	if not job_skills and suggested_roles:
		top_role = suggested_roles[0][1]
		job_skills = (
			{"python", "sql", "machine learning", "data science", "data analysis", "statistics"}
			if top_role == "Data Scientist"
			else ROLE_SKILLS[top_role.lower()]
		)
	matched = sorted(resume_skills & job_skills)
	missing = sorted(job_skills - resume_skills)

	sections = {
		label: any(re.search(r"(?im)^\s*" + re.escape(alias) + r"\s*:?\s*$", resume) for alias in aliases)
		for label, aliases in SECTION_NAMES.items()
	}
	bullets = re.findall(r"(?m)^\s*[•●*-]\s+.+$", resume)
	quantified = re.findall(r"\b\d+(?:\.\d+)?\s*(?:%|years?|months?|k|m|million|hours?|people|users?)?\b", resume_lower)
	word_count = len(re.findall(r"\b[\w+#.%-]+\b", resume))
	contact_signals = sum(bool(re.search(pattern, resume_lower)) for pattern in (r"[\w.+-]+@[\w-]+\.[\w.-]+", r"\b(?:\+?\d[\d ().-]{7,}\d)\b", r"linkedin\.com"))

	coverage = round((len(matched) / len(job_skills)) * 100) if job_skills else 0
	section_score = round(sum(sections.values()) / len(sections) * 100)
	impact_score = min(100, len(quantified) * 20 + min(len(bullets), 10) * 3)
	structure_score = min(100, section_score * 0.7 + min(contact_signals, 3) / 3 * 30)
	overall = round(coverage * 0.45 + section_score * 0.25 + impact_score * 0.2 + structure_score * 0.1) if job_skills else round(section_score * 0.45 + impact_score * 0.35 + structure_score * 0.2)

	recommendations = []
	if missing:
		recommendations.append("Add evidence for: " + ", ".join(missing[:8]) + ".")
	if not sections["summary"]:
		recommendations.append("Add a concise professional summary tailored to the target role.")
	if not sections["experience"]:
		recommendations.append("Use an Experience section with outcomes, scope, and ownership.")
	if not sections["skills"]:
		recommendations.append("Add a focused Skills section using the terminology from the job description.")
	if not quantified:
		recommendations.append("Quantify achievements with percentages, time saved, revenue, scale, or team size.")
	if word_count < 250:
		recommendations.append("The resume is quite short; add relevant evidence while keeping it focused.")
	if word_count > 900:
		recommendations.append("Consider trimming older or repetitive content to improve scanability.")
	if not recommendations:
		recommendations.append("Strong baseline. Tighten bullets around the role's highest-priority outcomes.")

	return {
		"overall": overall,
		"coverage": coverage,
		"section_score": section_score,
		"impact_score": round(impact_score),
		"word_count": word_count,
		"matched": matched,
		"missing": missing,
		"sections": sections,
		"recommendations": recommendations,
		"suggested_roles": suggested_roles,
	}


class ResumeAnalyzerApp(tk.Tk):
	def __init__(self):
		super().__init__()
		self.title("Resume Analyzer")
		self.geometry("1180x760")
		self.minsize(900, 620)
		self.configure(bg="#f4f1ea")
		self._build_styles()
		self._build_ui()

	def _build_styles(self):
		style = ttk.Style(self)
		style.theme_use("clam")
		style.configure("App.TFrame", background="#f4f1ea")
		style.configure("Panel.TFrame", background="#fffdf8")
		style.configure("Title.TLabel", background="#f4f1ea", foreground="#18211f", font=("Georgia", 28, "bold"))
		style.configure("Subtitle.TLabel", background="#f4f1ea", foreground="#65716d", font=("Segoe UI", 11))
		style.configure("PanelTitle.TLabel", background="#fffdf8", foreground="#18211f", font=("Segoe UI", 13, "bold"))
		style.configure("Muted.TLabel", background="#fffdf8", foreground="#71807a", font=("Segoe UI", 9))
		style.configure("Accent.TButton", background="#d86b45", foreground="white", font=("Segoe UI", 10, "bold"), padding=(14, 9))
		style.map("Accent.TButton", background=[("active", "#b95334")])
		style.configure("Secondary.TButton", background="#e8e2d7", foreground="#27332f", padding=(10, 8))

	def _build_ui(self):
		outer = ttk.Frame(self, style="App.TFrame", padding=28)
		outer.pack(fill="both", expand=True)
		header = ttk.Frame(outer, style="App.TFrame")
		header.pack(fill="x", pady=(0, 20))
		ttk.Label(header, text="Resume Analyzer", style="Title.TLabel").pack(anchor="w")
		ttk.Label(header, text="A clear-eyed review of your resume against the role you want next.", style="Subtitle.TLabel").pack(anchor="w", pady=(4, 0))

		workspace = ttk.Frame(outer, style="App.TFrame")
		workspace.pack(fill="both", expand=True)
		workspace.columnconfigure(0, weight=1)
		workspace.columnconfigure(1, weight=1)
		workspace.rowconfigure(0, weight=1)

		left = ttk.Frame(workspace, style="Panel.TFrame", padding=18)
		left.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
		right = ttk.Frame(workspace, style="Panel.TFrame", padding=18)
		right.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
		left.rowconfigure(2, weight=1)
		left.rowconfigure(4, weight=1)
		left.columnconfigure(0, weight=1)
		right.columnconfigure(0, weight=1)
		right.rowconfigure(3, weight=1)

		ttk.Label(left, text="Your resume", style="PanelTitle.TLabel").grid(row=0, column=0, sticky="w")
		ttk.Button(left, text="Open file", style="Secondary.TButton", command=self.open_resume).grid(row=0, column=0, sticky="e")
		ttk.Label(left, text="Paste text or open a TXT, Markdown, PDF, or DOCX file.", style="Muted.TLabel").grid(row=1, column=0, sticky="w", pady=(4, 8))
		self.resume_text = tk.Text(left, wrap="word", undo=True, font=("Segoe UI", 10), bg="#f8f5ef", fg="#27332f", insertbackground="#d86b45", relief="flat", padx=12, pady=10)
		self.resume_text.grid(row=2, column=0, sticky="nsew")
		ttk.Label(left, text="Target job description (optional)", style="PanelTitle.TLabel").grid(row=3, column=0, sticky="w", pady=(18, 0))
		self.job_text = tk.Text(left, wrap="word", height=8, undo=True, font=("Segoe UI", 10), bg="#f8f5ef", fg="#27332f", insertbackground="#d86b45", relief="flat", padx=12, pady=10)
		self.job_text.grid(row=4, column=0, sticky="nsew", pady=(8, 0))
		ttk.Button(left, text="Analyze resume", style="Accent.TButton", command=self.run_analysis).grid(row=5, column=0, sticky="e", pady=(16, 0))

		ttk.Label(right, text="Analysis snapshot", style="PanelTitle.TLabel").grid(row=0, column=0, sticky="w")
		self.score_label = ttk.Label(right, text="--", background="#fffdf8", foreground="#d86b45", font=("Georgia", 42, "bold"))
		self.score_label.grid(row=1, column=0, sticky="w", pady=(12, 0))
		self.score_note = ttk.Label(right, text="Add your resume and run an analysis.", style="Muted.TLabel")
		self.score_note.grid(row=2, column=0, sticky="w")
		self.results = tk.Text(right, wrap="word", state="disabled", font=("Segoe UI", 10), bg="#fffdf8", fg="#27332f", relief="flat", padx=2, pady=14)
		self.results.grid(row=3, column=0, sticky="nsew")
		self.results.tag_configure("heading", font=("Segoe UI", 11, "bold"), foreground="#18211f", spacing3=12)
		self.results.tag_configure("good", foreground="#35745b")
		self.results.tag_configure("warn", foreground="#b95334")

	def open_resume(self):
		file_path = filedialog.askopenfilename(
			title="Select your resume",
			filetypes=[
				("Text files", "*.txt"),
				("Markdown files", "*.md"),
				("PDF files", "*.pdf"),
				("Word documents", "*.docx"),
				("All files", "*.*"),
			],
		)
		if not file_path:
			return
		try:
			text = extract_text(file_path)
			if not text.strip():
				raise RuntimeError("No readable text was found in this file. Try a text-based PDF or paste the resume text.")
			self.resume_text.delete("1.0", "end")
			self.resume_text.insert("1.0", text)
		except Exception as error:
			messagebox.showerror("Could not open resume", str(error))

	def run_analysis(self):
		resume = self.resume_text.get("1.0", "end").strip()
		job_description = self.job_text.get("1.0", "end").strip()
		if not resume:
			messagebox.showwarning("Resume needed", "Paste your resume or open a resume file first.")
			return
		report = analyze_resume(resume, job_description)
		self.score_label.configure(text=f"{report['overall']}/100")
		self.score_note.configure(text="Overall resume readiness score")
		self.results.configure(state="normal")
		self.results.delete("1.0", "end")
		if report["suggested_roles"]:
			self.results.insert("end", "BEST-FIT ROLES\n", "heading")
			for score, role, matched, description in report["suggested_roles"][:3]:
				self.results.insert("end", f"{role}  -  {score}% fit\n", "good")
			self.results.insert("end", "Based on the skills detected in your resume. Add a job description for a role-specific comparison.\n\n")
		self.results.insert("end", "KEY SIGNALS\n", "heading")
		self.results.insert("end", f"Keyword match     {report['coverage']}%\n")
		self.results.insert("end", f"Structure          {report['section_score']}%\n")
		self.results.insert("end", f"Impact evidence    {report['impact_score']}%\n")
		self.results.insert("end", f"Resume length      {report['word_count']} words\n\n")
		self.results.insert("end", "MATCHED SKILLS\n", "heading")
		self.results.insert("end", (", ".join(report["matched"]) or "No target skills detected.") + "\n\n", "good")
		self.results.insert("end", "SKILLS TO CONSIDER\n", "heading")
		self.results.insert("end", (", ".join(report["missing"]) or "No obvious skill gaps detected.") + "\n\n", "warn" if report["missing"] else "good")
		self.results.insert("end", "RECOMMENDATIONS\n", "heading")
		for recommendation in report["recommendations"]:
			self.results.insert("end", f"• {recommendation}\n")
		self.results.configure(state="disabled")


if __name__ == "__main__":
	ResumeAnalyzerApp().mainloop()
