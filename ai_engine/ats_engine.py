import re


def calculate_ats(semantic, resume_skills, job_skills, resume_text=""):

    # ---------- CLEAN TEXT ----------
    text = re.sub(r"\s+", " ", resume_text.lower())

    resume_skills = set(resume_skills)
    job_skills = set(job_skills)

    # ---------- SKILL MATCH ----------
    if job_skills:
        skill_match = (len(resume_skills & job_skills) / len(job_skills)) * 100
    else:
        skill_match = 50   # Neutral if no job skills

    # ---------- SKILL RELEVANCE ----------
    if resume_skills:
        relevance = (len(resume_skills & job_skills) / len(resume_skills)) * 100
    else:
        relevance = 0

    # ---------- RESUME QUALITY ----------
    quality_score = 0

    quality_keywords = {
        "project": 20,
        "intern": 20,
        "experience": 20,
        "github": 10,
        "portfolio": 10,
        "certification": 10,
        "course": 10
    }

    for keyword, weight in quality_keywords.items():
        if keyword in text:
            quality_score += weight

    quality_score = min(quality_score, 100)

    # ---------- FINAL ATS SCORE ----------
    ats_score = (
        0.35 * semantic +
        0.40 * skill_match +
        0.15 * relevance +
        0.10 * quality_score
    )

    return round(min(ats_score, 100), 2)
