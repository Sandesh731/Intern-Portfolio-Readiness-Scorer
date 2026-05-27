# 🎯 Intern Portfolio Readiness Scorer

> An AI/ML-powered resume analytics system that predicts intern employability and provides personalized portfolio improvement recommendations.

**Developed for:** Graphura India Private Limited  
**Domain:** Data Analytics | Machine Learning | Flask API | Power BI  
**Dataset:** 572 Intern Profiles | 5 Domains | 3 Readiness Classes

---

## 📌 Table of Contents

- [Overview](#-overview)
- [Problem Statement](#-problem-statement)
- [Features](#-features)
- [System Architecture](#-system-architecture)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Dataset](#-dataset)
- [ML Model](#-ml-model)
- [Scoring Algorithm](#-scoring-algorithm)
- [API Endpoints](#-api-endpoints)
- [Dashboard KPIs](#-dashboard-kpis)
- [Installation & Setup](#-installation--setup)
- [Usage](#-usage)
- [Results](#-results)
- [Future Scope](#-future-scope)
- [License](#-license)

---

## 📖 Overview

The **Intern Portfolio Readiness Scorer** is a full-stack AI/ML web application that automates the evaluation of intern portfolios. It parses PDF/DOCX resumes, extracts key features using NLP-based keyword matching, computes a weighted readiness score, and runs a Random Forest classifier to predict employability — all via a Flask REST API with a clean frontend UI and a Power BI analytics dashboard for management.

---

## ❗ Problem Statement

Portfolio quality at Graphura was evaluated **manually and subjectively**, making it:
- Inconsistent across intern batches
- Difficult to scale as intern numbers grow
- Unable to provide structured, actionable feedback
- Incapable of predicting industry placement readiness

This project replaces manual review with a **standardized, data-driven scoring pipeline**.

---

## ✨ Features

- 📄 **Resume Parsing** — Extracts text from PDF and DOCX resumes using `pdfplumber` and `python-docx`
- 🔍 **Keyword Detection** — Identifies 30+ tools/technologies, projects, certifications, documentation
- 📊 **Hybrid Scoring Engine** — Weighted rule-based formula (70%) + Random Forest ML (30%)
- 🤖 **ML Prediction** — Classifies interns as *Job Ready*, *Almost Ready*, or *Needs Improvement*
- 💡 **Recommendation System** — Auto-generates strengths, weaknesses, and improvement suggestions
- 🌐 **Flask REST API** — Clean `/score` endpoint returning full JSON analytics
- 📱 **Web Frontend** — Responsive HTML/CSS/JS interface with drag-and-drop resume upload
- 📈 **Power BI Dashboard** — Interactive management dashboard with KPIs and trend analysis

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        INPUT LAYER                          │
│          PDF / DOCX Resume  →  HTML Frontend Upload         │
└───────────────────────────┬─────────────────────────────────┘
                            │ POST /score
┌───────────────────────────▼─────────────────────────────────┐
│                     PROCESSING LAYER                        │
│                                                             │
│  pdfplumber / python-docx  →  Text Extraction               │
│         ↓                                                   │
│  parse_resume()  →  Feature Engineering (13 features)       │
│         ↓                                                   │
│  rule_based_score()   →   Weighted Score (0–100)            │
│  ml_predict()         →   Random Forest Prediction          │
│  generate_recommendations()  →  Strengths/Gaps/Tips         │
└───────────────────────────┬─────────────────────────────────┘
                            │ JSON Response
┌───────────────────────────▼─────────────────────────────────┐
│                       OUTPUT LAYER                          │
│   Readiness Score  |  Category  |  Confidence  |  Tips      │
│              Power BI Analytics Dashboard                   │
└─────────────────────────────────────────────────────────────┘
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python 3.x, Flask, Flask-CORS |
| ML/AI | Scikit-Learn (Random Forest), StandardScaler |
| Text Extraction | pdfplumber, python-docx |
| Data Processing | Pandas, NumPy |
| Model Persistence | Joblib (.pkl files) |
| Frontend | HTML5, CSS3, JavaScript (Fetch API) |
| Dashboard | Power BI Desktop |
| Dataset | Excel (.xlsx) — 572 records |

---

## 📁 Project Structure

```
intern-portfolio-readiness-scorer/
│
├── app.py                                      # Flask backend + API
├── index.html                                  # Frontend UI
│
├── model.pkl                                   # Trained Random Forest model
├── scaler.pkl                                  # StandardScaler for normalization
├── feature_names.pkl                           # Feature column names
│
├── intern_dataset_572.xlsx                     # Raw intern dataset (572 records)
├── Final_dataset.xlsx                          # Processed dataset
├── Intern_Readiness_Results.xlsx               # Model output results
│
├── Intern_Portfolio_Readiness_Scorer.ipynb     # ML training notebook
│
├── Intern_Portfolio_Readiness_Analytics_       # Power BI dashboard (PDF export)
│   dashboard.pdf
├── Intern_Portfolio_Readiness_Scorer.pdf       # Project brief
│
└── README.md
```

---

## 📊 Dataset

| Attribute | Value |
|-----------|-------|
| Total Records | 572 intern profiles |
| Domains | Machine Learning, Data Analytics, Data Science, Web Development, Python Development |
| Features | 13 (7 base + 5 domain one-hot encoded + target) |
| Target Classes | Job Ready / Almost Ready / Needs Improvement |
| Class Distribution | 62.24% Almost Ready · 21.85% Needs Improvement · 15.91% Job Ready |
| Average Portfolio Score | 6.86 / 10 |

### Features Used

| Feature | Type | Description |
|---------|------|-------------|
| `Number_of_Projects` | Integer | Estimated project count from resume |
| `Number_of_Repository` | Integer | GitHub repo count proxy |
| `Tools_Count` | Integer | Number of technologies detected |
| `Has_README` | Binary | Documentation presence (0/1) |
| `Has_Certification` | Binary | Certification presence (0/1) |
| `Technical_Skill_Score` | Float 0–10 | Score based on tools detected |
| `Project_Quality_Score` | Float 0–10 | Score based on quality keywords |
| `Domain_*` | One-Hot | 5 binary domain flags |

---

## 🤖 ML Model

- **Algorithm:** Random Forest Classifier (ensemble of decision trees)
- **Train/Test Split:** 80% / 20% (stratified)
- **Preprocessing:** StandardScaler normalization
- **Output:** Class prediction + `predict_proba()` confidence score
- **Serialized:** `model.pkl`, `scaler.pkl`, `feature_names.pkl` via Joblib

---

## ⚖️ Scoring Algorithm

The rule-based score is computed as a weighted sum across 7 dimensions:

```
Score = (Project_Quality_Score × 0.30)
      + (Technical_Skill_Score × 0.25)
      + (Num_Projects_norm     × 0.15)
      + (Tools_Count_norm      × 0.10)
      + (Has_Certification     × 0.08 × 10)
      + (Has_README            × 0.07 × 10)
      + (Num_Repos_norm        × 0.05)

Final Score = min(100, Score × 10)
```

**Readiness Categories:**

| Score Range | Category |
|-------------|----------|
| ≥ 75 | ✅ Job Ready |
| 50 – 74 | 🟡 Almost Ready |
| < 50 | 🔴 Needs Improvement |

---

## 🔌 API Endpoints

### `GET /`
Serves the frontend HTML interface.

### `POST /score`
Accepts a resume file and returns full portfolio analysis.

**Request:**
```
Content-Type: multipart/form-data
Body: resume = <file.pdf or file.docx>
```

**Response (JSON):**
```json
{
  "rule_score": 82.5,
  "rule_category": "Job Ready",
  "ml_category": "Job Ready",
  "ml_confidence": 91.2,
  "domain": "Machine Learning",
  "tools_found": ["python", "pandas", "tensorflow", "flask", "github"],
  "tools_count": 5,
  "num_projects": 6,
  "has_certification": 1,
  "has_readme": 1,
  "technical_skill_score": 8.5,
  "project_quality_score": 7.8,
  "strengths": ["Strong project quality", "Good technical skills", "Certifications present hain"],
  "weaknesses": [],
  "suggestions": []
}
```

---

## 📈 Dashboard KPIs

Built with Power BI Desktop on the 572-intern dataset:

| KPI | Value |
|-----|-------|
| Total Interns | 572 |
| Average Portfolio Score | 6.86 / 10 |
| Job Ready | 91 (15.91%) |
| Almost Ready | 356 (62.24%) |
| Needs Improvement | 125 (21.85%) |
| Top Performer | Ayaan Khan — 30.6 |

**Visualizations:**
- Readiness Distribution (Donut Chart)
- Top 10 Performer Leaderboard (Bar Chart)
- Domain-wise Average Score Comparison
- Category-wise Skill Breakdown (Technical, Certification, Presentation, Project Quality)
- Interactive Intern Name Slicer

---

## ⚙️ Installation & Setup

### Prerequisites

```bash
Python 3.8+
pip
```

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/intern-portfolio-readiness-scorer.git
cd intern-portfolio-readiness-scorer
```

### 2. Install Dependencies

```bash
pip install flask flask-cors pdfplumber python-docx pandas numpy scikit-learn joblib openpyxl
```

### 3. Run the Application

```bash
python app.py
```

The app will start at: `http://localhost:5000`

> **Note:** `model.pkl`, `scaler.pkl`, and `feature_names.pkl` must be present in the root directory. The app will log `Model loaded successfully!` on startup if they are found.

---

## 🚀 Usage

1. Open `http://localhost:5000` in your browser
2. Click **Upload Resume** and select a PDF or DOCX file
3. Click **Analyze Portfolio**
4. View your:
   - Readiness Score (0–100)
   - Category (Job Ready / Almost Ready / Needs Improvement)
   - ML Confidence %
   - Detected Technologies
   - Strengths & Improvement Suggestions

---

## 📊 Results

| Metric | Value |
|--------|-------|
| Dataset Size | 572 profiles |
| ML Algorithm | Random Forest Classifier |
| Readiness Classes | 3 |
| Tools Vocabulary | 30 keywords |
| Domains Supported | 5 |
| API Response Time | < 2 seconds |
| Rule Score Weight | 70% |
| ML Score Weight | 30% |

---

## 🔮 Future Scope

- [ ] **LLM-Based Parsing** — Replace keyword matching with BERT/GPT for semantic understanding
- [ ] **GitHub API Integration** — Fetch live repo counts, commit history, and README quality
- [ ] **Batch Processing** — Score multiple resumes in a single API call
- [ ] **Cloud Deployment** — Docker + AWS/GCP production deployment
- [ ] **Mobile App** — React Native app for on-device resume scanning
- [ ] **Industry Benchmarking** — Compare scores against domain-specific industry standards
- [ ] **Interview Prep Module** — Suggest domain-specific courses and practice resources

---

## 📄 License

This project was developed as part of an internship at **Graphura India Private Limited**.  
All rights reserved © 2026 Graphura India Pvt. Ltd.

---

<div align="center">
  <strong>Developed at Graphura India Private Limited · May 2026</strong><br>
  Data Analytics | Machine Learning | Flask | Power BI
</div>
