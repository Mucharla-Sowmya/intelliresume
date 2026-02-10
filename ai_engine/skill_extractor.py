import spacy

nlp = spacy.load("en_core_web_sm")

# Known technical skills list
SKILL_DB = [
    "python", "java", "sql", "html", "css", "javascript",
    "react", "node.js", "django", "flask",
    "machine learning", "tensorflow", "ai",
    "power bi", "firebase", "git", "github",
    "openai", "azure", "dbms"
]


def extract_skills_ai(text):

    text = text.lower()

    detected_skills = []

    for skill in SKILL_DB:
        if skill in text:
            detected_skills.append(skill)

    return list(set(detected_skills))
