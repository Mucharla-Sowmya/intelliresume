import PyPDF2
import docx


def extract_text(file_path):

    text = ""

    # PDF Extraction
    if file_path.endswith(".pdf"):
        with open(file_path, "rb") as file:
            reader = PyPDF2.PdfReader(file)

            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text

    # DOCX Extraction
    elif file_path.endswith(".docx"):
        doc = docx.Document(file_path)

        for para in doc.paragraphs:
            text += para.text + "\n"

    return text
