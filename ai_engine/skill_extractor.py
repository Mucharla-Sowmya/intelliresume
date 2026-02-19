import spacy
from spacy.matcher import PhraseMatcher

nlp = spacy.load("en_core_web_sm")

# Expanded skill database
SKILL_DB = [
    "python", "java", "sql", "html", "css", "javascript",
    "react", "reactjs", "node.js", "nodejs",
    "django", "flask",
    "machine learning", "deep learning",
    "tensorflow", "pytorch", "ai",
    "power bi", "tableau",
    "firebase", "git", "github",
    "openai", "azure", "aws",
    "dbms", "mongodb", "postgresql"
]

# Phrase matcher setup
matcher = PhraseMatcher(nlp.vocab, attr="LOWER")
patterns = [nlp.make_doc(skill) for skill in SKILL_DB]
matcher.add("SKILLS", patterns)


def extract_skills_ai(text):

    doc = nlp(text)

    detected_skills = set()

    # Phrase matching
    matches = matcher(doc)
    for _, start, end in matches:
        detected_skills.add(doc[start:end].text.lower())

    return list(detected_skills)
