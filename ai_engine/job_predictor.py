ROLE_MAP = {
    "Data Scientist": ["python", "machine learning", "sql", "statistics"],
    "AI Engineer": ["python", "deep learning", "tensorflow"],
    "Web Developer": ["html", "css", "javascript", "flask"],
    "Backend Developer": ["python", "django", "api", "sql"]
}


def predict_job_role(skills):

    best_role = "General Candidate"
    max_score = 0

    for role, role_skills in ROLE_MAP.items():

        # Count matching skills
        score = len(set(skills) & set(role_skills))

        if score > max_score:
            max_score = score
            best_role = role

    return best_role
