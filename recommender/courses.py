# Expanded course database
COURSE_DB = {
    "python": "Python for Everybody – Coursera",
    "machine learning": "Machine Learning by Andrew Ng – Coursera",
    "deep learning": "DeepLearning.AI Specialization – Coursera",
    "sql": "Google Data Analytics SQL Course",
    "html": "HTML & CSS Bootcamp – Udemy",
    "css": "Frontend Web Development – Coursera",
    "javascript": "JavaScript Complete Guide – Udemy",
    "react": "React Developer Course – Meta",
    "node.js": "Node.js Backend Development – Udemy",
    "django": "Django Full Stack Course – Coursera",
    "flask": "Python Flask Bootcamp – Udemy",
    "ai": "AI Foundations – IBM Coursera",
    "tensorflow": "TensorFlow Developer Certificate",
    "pytorch": "PyTorch Deep Learning Course",
    "aws": "AWS Cloud Practitioner – Amazon",
    "azure": "Microsoft Azure Fundamentals",
    "docker": "Docker & Kubernetes Bootcamp",
    "mongodb": "MongoDB Developer Course",
    "postgresql": "PostgreSQL Database Course",
    "power bi": "Microsoft Power BI Certification",
    "tableau": "Tableau Data Visualization Course",
    "git": "Git & GitHub Crash Course"
}


def recommend_courses(missing_skills):

    recommendations = []

    for skill in missing_skills:

        skill_lower = skill.lower().strip()

        # Exact match
        if skill_lower in COURSE_DB:
            recommendations.append({
                "skill": skill,
                "course": COURSE_DB[skill_lower]
            })

        # Partial match fallback
        else:
            for key in COURSE_DB:
                if key in skill_lower or skill_lower in key:
                    recommendations.append({
                        "skill": skill,
                        "course": COURSE_DB[key]
                    })
                    break

    # Remove duplicates
    unique = []
    seen = set()

    for r in recommendations:
        if r["skill"] not in seen:
            unique.append(r)
            seen.add(r["skill"])

    return unique
