from flask import Flask, render_template, request
import os

from resume_parser.parser import extract_text
from ai_engine.bert_matcher import semantic_similarity
from ai_engine.skill_extractor import extract_skills_ai
from ai_engine.ats_engine import calculate_ats
from recommender.courses import recommend_courses
from ai_engine.ai_job_predictor import ai_predict_job_role


app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Ensure uploads folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route("/")
def home():
    return render_template("home.html")


# ===================== APPLICANT ROUTE =====================
@app.route("/applicant", methods=["GET", "POST"])
def applicant():

    if request.method == "POST":

        file = request.files["resume"]
        job_desc = request.form["job"]

        # Save resume
        path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
        file.save(path)

        # Extract text
        resume_text = extract_text(path)

        # Semantic similarity
        semantic = semantic_similarity(resume_text, job_desc)

        # Skill extraction
        resume_skills = extract_skills_ai(resume_text)
        job_skills = extract_skills_ai(job_desc)

        # ATS score
        ats = calculate_ats(semantic, resume_skills, job_skills)

        # AI job role prediction
        predicted_role = ai_predict_job_role(resume_text)

        # Missing skills
        missing_skills = list(set(job_skills) - set(resume_skills))

        # Course recommendations
        courses = recommend_courses(missing_skills)

        # ⭐ RETURN RESULT PAGE (NO FEEDBACK)
        return render_template(
            "result.html",
            semantic=semantic,
            ats=ats,
            role=predicted_role,
            skills=resume_skills,
            courses=courses
        )

    return render_template("applicant.html")


# ===================== RECRUITER ROUTE =====================
@app.route("/recruiter", methods=["GET", "POST"])
def recruiter():

    if request.method == "POST":

        files = request.files.getlist("resumes")
        job_desc = request.form["job"]

        results = []

        for file in files:

            path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
            file.save(path)

            resume_text = extract_text(path)

            score = semantic_similarity(resume_text, job_desc)

            results.append({
                "name": file.filename,
                "score": round(score, 2)
            })

        results.sort(key=lambda x: x["score"], reverse=True)

        return render_template("recruiter_result.html", results=results)

    return render_template("recruiter.html")


if __name__ == "__main__":
    app.run(debug=True)
