from flask import Flask, render_template, request, redirect, url_for, session, flash
import os
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

# AI Modules
from resume_parser.parser import extract_text
from ai_engine.bert_matcher import semantic_similarity
from ai_engine.skill_extractor import extract_skills_ai
from ai_engine.ats_engine import calculate_ats
from recommender.courses import recommend_courses
from ai_engine.ai_job_predictor import ai_predict_job_role

app = Flask(__name__)
app.secret_key = "intelliresume_secret"

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# ---------------- DATABASE ----------------

def init_db():
    conn = sqlite3.connect("users.db")
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        email TEXT UNIQUE,
        password TEXT
    )
    """)

    conn.commit()
    conn.close()


init_db()


# ---------------- ADVANCED SKILLS ----------------

ADVANCED_SKILLS = {
    "Web Developer": ["typescript", "next.js", "graphql"],
    "Backend Developer": ["redis", "docker", "microservices"],
    "Data Scientist": ["pandas", "mlops", "feature engineering"],
    "AI Engineer": ["transformers", "llm fine tuning"],
    "Cloud Engineer": ["terraform", "kubernetes"]
}


# ---------------- LOGIN ----------------

@app.route("/", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        conn = sqlite3.connect("users.db")
        cur = conn.cursor()

        cur.execute("SELECT * FROM users WHERE email=?", (email,))
        user = cur.fetchone()

        conn.close()

        if user and check_password_hash(user[3], password):

            session["user"] = user[1]
            flash("Login Successful!", "success")

            return redirect(url_for("home"))

        else:
            flash("Invalid Email or Password", "danger")

    return render_template("login.html")


# ---------------- REGISTER ----------------

@app.route("/register", methods=["GET", "POST"])
@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        hashed_password = generate_password_hash(password)

        conn = sqlite3.connect("users.db")
        cur = conn.cursor()

        # Check if email already exists
        cur.execute("SELECT * FROM users WHERE email=?", (email,))
        existing_user = cur.fetchone()

        if existing_user:
            flash("⚠ Email already registered! Please use another email.", "danger")
            conn.close()
            return render_template("register.html")

        # Insert new user
        cur.execute(
            "INSERT INTO users(username,email,password) VALUES(?,?,?)",
            (username, email, hashed_password)
        )

        conn.commit()
        conn.close()

        flash("✅ Registration successful! Please login.", "success")

        return redirect(url_for("login"))

    return render_template("register.html")


# ---------------- LOGOUT ----------------

@app.route("/logout")
def logout():

    session.pop("user", None)
    flash("Logged out successfully", "info")

    return redirect(url_for("login"))


# ---------------- HOME ----------------

@app.route("/home")
def home():

    if "user" not in session:
        return redirect(url_for("login"))

    return render_template("home.html")


# ---------------- APPLICANT ----------------

@app.route("/applicant", methods=["GET", "POST"])
def applicant():

    if "user" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":

        file = request.files["resume"]
        job_desc = request.form["job"]

        path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
        file.save(path)

        # Extract resume text
        resume_text = extract_text(path)

        # Semantic similarity
        semantic = semantic_similarity(resume_text, job_desc)

        # Skill extraction
        resume_skills = extract_skills_ai(resume_text)
        job_skills = extract_skills_ai(job_desc)

        # Normalize
        resume_skills = [s.lower() for s in resume_skills]
        job_skills = [s.lower() for s in job_skills]

        # Predict role
        predicted_role = ai_predict_job_role(resume_text)

        # Missing skills
        missing_skills = list(set(job_skills) - set(resume_skills))

        # If no missing skills recommend advanced
        if not missing_skills:
            missing_skills = ADVANCED_SKILLS.get(predicted_role, [])

        # Course recommendations
        courses = recommend_courses(missing_skills)

        # ATS Score
        ats = calculate_ats(
            semantic,
            resume_skills,
            job_skills,
            resume_text
        )

        return render_template(
            "result.html",
            semantic=semantic,
            ats=ats,
            role=predicted_role,
            skills=resume_skills,
            courses=courses
        )

    return render_template("applicant.html")


# ---------------- RECRUITER ----------------

@app.route("/recruiter", methods=["GET", "POST"])
def recruiter():

    if "user" not in session:
        return redirect(url_for("login"))

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

        return render_template(
            "recruiter_result.html",
            results=results
        )

    return render_template("recruiter.html")


# ---------------- MAIN ----------------

if __name__ == "__main__":
    app.run(debug=True)