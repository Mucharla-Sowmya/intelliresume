COURSE_DB = {
    "python": "Coursera Python Specialization",
    "machine learning": "Andrew Ng Machine Learning Course",
    "sql": "Google SQL Course",
    "deep learning": "DeepLearning.AI Course",
    "flask": "Udemy Flask Bootcamp",
    "html": "HTML & CSS Crash Course",
    "javascript": "JavaScript Bootcamp"
}


def recommend_courses(missing_skills):

    recommendations = []

    for skill in missing_skills:
        if skill.lower() in COURSE_DB:
            recommendations.append({
                "skill": skill,
                "course": COURSE_DB[skill.lower()]
            })

    return recommendations
