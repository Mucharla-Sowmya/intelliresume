import google.generativeai as genai
import json

genai.configure(api_key="API_KEY")

def extract_resume_info(pdf_text):

    model = genai.GenerativeModel("gemini-1.5-flash")

    prompt = f"""
    Extract the following from the resume text below into a clean JSON object:

    candidate_name
    technical_skills (list)
    current_role
    years_of_experience

    Resume Text:
    {pdf_text}
    """

    response = model.generate_content(prompt)

    json_data = response.text.replace("```json", "").replace("```", "").strip()

    return json.loads(json_data)