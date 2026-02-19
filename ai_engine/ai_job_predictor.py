from transformers import pipeline

# Zero-shot AI classifier
classifier = pipeline("zero-shot-classification",
                    model="facebook/bart-large-mnli")


def ai_predict_job_role(resume_text):

    labels = [
        "Data Scientist",
        "AI Engineer",
        "Web Developer",
        "Backend Developer",
        "Frontend Developer",
        "Software Engineer",
        "Cloud Engineer",
        "Data Analyst",
        "Machine Learning Engineer",
        "DevOps Engineer",
        "Python Developer",
        "Java Developer"
    ]

    result = classifier(resume_text[:1000], labels)

    return result["labels"][0]
