def calculate_ats(semantic_score, resume_skills, job_skills):

    # If no job skills detected
    if len(job_skills) == 0:
        return semantic_score

    # Count matched skills
    matched = len(set(resume_skills) & set(job_skills))

    # Skill match percentage
    skill_score = (matched / len(job_skills)) * 100

    # Final ATS Score calculation
    ats_score = (semantic_score * 0.6) + (skill_score * 0.4)

    return round(ats_score, 2)
