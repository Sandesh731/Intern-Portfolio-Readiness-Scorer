from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import pdfplumber
import docx
import pandas as pd
import numpy as np
import re
import os
import joblib

app = Flask(__name__)
CORS(app)

TOOLS_KEYWORDS = [
    'python','sql','tableau','power bi','excel','pandas','numpy',
    'matplotlib','seaborn','scikit','tensorflow','keras','flask',
    'django','react','javascript','html','css','node','mongodb',
    'mysql','postgresql','r studio','spark','hadoop','git','github',
    'machine learning','deep learning','nlp','opencv','fastapi'
]

try:
    rf_model = joblib.load('model.pkl')
    scaler = joblib.load('scaler.pkl')
    feature_names = joblib.load('feature_names.pkl')
    print("Model loaded successfully!")
except Exception as e:
    print(f"Model load error: {e}")
    rf_model = None
    scaler = None
    feature_names = None

def extract_text_from_pdf(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text

def extract_text_from_docx(file):
    doc = docx.Document(file)
    text = "\n".join([para.text for para in doc.paragraphs])
    return text

def parse_resume(text):
    text_lower = text.lower()

    tools_found = [tool for tool in TOOLS_KEYWORDS if tool in text_lower]
    tools_count = len(tools_found)

    project_keywords = ['project','built','developed','created','designed','implemented','deployed']
    project_count = sum(1 for kw in project_keywords if kw in text_lower)
    num_projects = min(project_count * 2, 15)

    repo_keywords = ['github','repository','repositories','repo']
    num_repos = sum(1 for kw in repo_keywords if kw in text_lower) * 5

    has_readme = 1 if 'readme' in text_lower or 'documentation' in text_lower else 0

    cert_keywords = ['certificate','certification','certified','coursera','udemy',
                     'google','microsoft','aws','linkedin learning','hackerrank','kaggle']
    has_certification = 1 if any(kw in text_lower for kw in cert_keywords) else 0

    tech_score = min(10, tools_count * 1.2 + 2)

    quality_keywords = ['analysis','machine learning','deep learning','visualization',
                        'dashboard','model','prediction','classification','regression',
                        'clustering','nlp','computer vision','api','deployment']
    quality_score = min(10, sum(1 for kw in quality_keywords if kw in text_lower) * 1.2 + 3)

    domain = "Data Analytics"
    if any(kw in text_lower for kw in ['machine learning','deep learning','tensorflow','keras','neural','nlp']):
        domain = "Machine Learning"
    elif any(kw in text_lower for kw in ['web','react','javascript','html','css','node','frontend','backend']):
        domain = "Web Development"
    elif any(kw in text_lower for kw in ['data science','statistics','r studio','statistical','scipy']):
        domain = "Data Science"
    elif any(kw in text_lower for kw in ['flask','django','fastapi','python developer']):
        domain = "Python Development"

    return {
        "tools_found": tools_found,
        "tools_count": tools_count,
        "num_projects": num_projects,
        "num_repos": num_repos,
        "has_readme": has_readme,
        "has_certification": has_certification,
        "technical_skill_score": round(tech_score, 1),
        "project_quality_score": round(quality_score, 1),
        "domain": domain
    }

def rule_based_score(parsed):
    projects_norm = min(10, parsed['num_projects'] * 1.2)
    tools_norm = min(10, parsed['tools_count'] * 1.1)
    repos_norm = min(10, parsed['num_repos'] * 0.4)

    score = (
        parsed['project_quality_score'] * 0.30 +
        parsed['technical_skill_score'] * 0.25 +
        projects_norm * 0.15 +
        tools_norm * 0.10 +
        parsed['has_certification'] * 0.08 * 10 +
        parsed['has_readme'] * 0.07 * 10 +
        repos_norm * 0.05
    )
    return min(100, round(score * 10, 1))

def get_category(score):
    if score >= 75:
        return "Job Ready"
    elif score >= 50:
        return "Almost Ready"
    else:
        return "Needs Improvement"

def ml_predict(parsed):
    if rf_model is None:
        return None, None
    try:
        input_data = {col: 0 for col in feature_names}
        input_data['Project_Quality_Score'] = parsed['project_quality_score']
        input_data['Technical_Skill_Score'] = parsed['technical_skill_score']
        input_data['Number_of_Repository'] = parsed['num_repos']
        input_data['Number_of_Projects'] = parsed['num_projects']
        input_data['Tools_Count'] = parsed['tools_count']
        input_data['Has_README'] = parsed['has_readme']
        input_data['Has_Certification'] = parsed['has_certification']

        domain_col = f"Domain_{parsed['domain']}"
        if domain_col in input_data:
            input_data[domain_col] = 1

        df_input = pd.DataFrame([input_data])[feature_names]
        df_scaled = scaler.transform(df_input)

        prediction = rf_model.predict(df_scaled)[0]
        proba = rf_model.predict_proba(df_scaled)[0]

        return prediction, round(float(max(proba)) * 100, 1)

    except Exception as e:
        print(f"ML prediction error: {e}")
        return None, None

def generate_recommendations(parsed):
    strengths = []
    weaknesses = []
    suggestions = []

    if parsed['project_quality_score'] >= 7:
        strengths.append("Strong project quality")
    else:
        weaknesses.append("Project quality weak hai")
        suggestions.append("Real-world projects banao — Kaggle competitions try karo")

    if parsed['technical_skill_score'] >= 7:
        strengths.append("Good technical skills")
    else:
        weaknesses.append("Technical skills improve karni hain")
        suggestions.append("Apne domain ki advanced tools seekho")

    if parsed['has_certification']:
        strengths.append("Certifications present hain")
    else:
        weaknesses.append("Koi certification nahi mili")
        suggestions.append("Google, Coursera ya LinkedIn pe free certifications lo")

    if parsed['has_readme']:
        strengths.append("Documentation achhi hai")
    else:
        weaknesses.append("README ya documentation missing")
        suggestions.append("Har GitHub project mein README zaroor likho")

    if parsed['tools_count'] >= 4:
        strengths.append("Achhi tool variety hai")
    else:
        weaknesses.append("Limited tools use kiye hain")
        suggestions.append("Apne domain ke 2-3 aur tools seekho")

    if parsed['num_projects'] >= 3:
        strengths.append("Achhe number of projects hain")
    else:
        weaknesses.append("Projects kam hain resume mein")
        suggestions.append("Kam se kam 3-5 complete projects banao aur mention karo")

    return strengths, weaknesses, suggestions

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/score', methods=['POST'])
def score_resume():
    if 'resume' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['resume']
    filename = file.filename.lower()

    try:
        if filename.endswith('.pdf'):
            text = extract_text_from_pdf(file)
        elif filename.endswith('.docx'):
            text = extract_text_from_docx(file)
        else:
            return jsonify({'error': 'Only PDF or DOCX supported'}), 400

        parsed = parse_resume(text)
        rule_score = rule_based_score(parsed)
        rule_category = get_category(rule_score)
        ml_category, ml_confidence = ml_predict(parsed)

        strengths, weaknesses, suggestions = generate_recommendations(parsed)

        return jsonify({
            "rule_score": rule_score,
            "rule_category": rule_category,
            "ml_category": ml_category or rule_category,
            "ml_confidence": ml_confidence or 0,
            "domain": parsed['domain'],
            "tools_found": parsed['tools_found'],
            "tools_count": parsed['tools_count'],
            "num_projects": parsed['num_projects'],
            "has_certification": parsed['has_certification'],
            "has_readme": parsed['has_readme'],
            "technical_skill_score": parsed['technical_skill_score'],
            "project_quality_score": parsed['project_quality_score'],
            "strengths": strengths,
            "weaknesses": weaknesses,
            "suggestions": suggestions
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)