import re

SKILL_DB = [
    "python","java","sql","html","css","javascript","react","node.js",
    "django","flask","mongodb","postgresql","mysql","git","github",
    "docker","kubernetes","aws","azure","tensorflow","pytorch",
    "machine learning","deep learning","ai","data science","pandas",
    "numpy","power bi","tableau","redis","graphql","typescript"
]


def extract_skills_ai(text):

    text = text.lower()

    detected_skills = set()

    for skill in SKILL_DB:

        pattern = r"\b" + re.escape(skill) + r"\b"

        if re.search(pattern, text):
            detected_skills.add(skill)

    return list(detected_skills)