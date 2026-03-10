def calculate_ats(semantic, resume_skills, job_skills, resume_text=""):

    resume_skills = set(resume_skills)
    job_skills = set(job_skills)

    # -------- Skill Match --------
    if job_skills:
        skill_match = (len(resume_skills & job_skills) / len(job_skills)) * 100
    else:
        skill_match = 60

    # -------- Resume Quality --------
    text = resume_text.lower()

    quality_score = 0

    if "project" in text:
        quality_score += 20

    if "experience" in text or "intern" in text:
        quality_score += 20

    if "github" in text:
        quality_score += 10

    if "portfolio" in text:
        quality_score += 10

    if "certification" in text:
        quality_score += 10

    if "course" in text:
        quality_score += 10

    quality_score = min(quality_score, 60)

    # -------- Final ATS --------
    ats_score = (
        0.4 * semantic +
        0.4 * skill_match +
        0.2 * quality_score
    )

    return round(min(ats_score,100),2)