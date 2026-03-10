import google.generativeai as genai
import json

genai.configure(api_key="API_KEY")

model = genai.GenerativeModel("gemini-1.5-flash-latest")


# fallback course database
COURSE_DB = {
    "typescript": "TypeScript Complete Guide – Udemy",
    "next.js": "Next.js Bootcamp – Udemy",
    "web security": "Web Security Fundamentals – Coursera",
    "machine learning": "Machine Learning by Andrew Ng – Coursera",
    "deep learning": "Deep Learning Specialization – Coursera",
    "mlops": "MLOps Fundamentals – Coursera",
    "redis": "Redis Crash Course – Udemy",
    "microservices": "Microservices Architecture – Udemy",
    "system design": "System Design Interview Course – Educative",
    "terraform": "Terraform for Cloud – Udemy",
    "kubernetes": "Kubernetes Masterclass – Udemy",
    "cloud architecture": "Cloud Architecture Course – Coursera"
}


def recommend_courses(missing_skills):

    if not missing_skills:
        return []

    try:

        skills_text = ", ".join(missing_skills)

        prompt = f"""
Recommend ONE high quality course for each skill below.

Skills:
{skills_text}

Return ONLY JSON like this:

[
 {{"skill":"python","course":"Python for Everybody – Coursera"}},
 {{"skill":"react","course":"React Complete Guide – Udemy"}}
]
"""

        response = model.generate_content(prompt)

        clean = response.text.replace("```json", "").replace("```", "").strip()

        courses = json.loads(clean)

        return courses

    except Exception as e:

        print("Gemini failed, using fallback courses")

        # fallback logic
        recommendations = []

        for skill in missing_skills:

            course = COURSE_DB.get(
                skill.lower(),
                f"Learn {skill} from Coursera or Udemy"
            )

            recommendations.append({
                "skill": skill,
                "course": course
            })

        return recommendations