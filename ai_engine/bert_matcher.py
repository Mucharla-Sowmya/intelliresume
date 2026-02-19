from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import re

# Better model
model = SentenceTransformer('all-MiniLM-L6-v2')


def semantic_similarity(resume_text, job_text):

    # Clean text
    resume_text = re.sub(r'\s+', ' ', resume_text)
    job_text = re.sub(r'\s+', ' ', job_text)

    # Convert to embeddings
    embeddings = model.encode(
        [resume_text, job_text],
        normalize_embeddings=True
    )

    similarity = cosine_similarity(
        [embeddings[0]],
        [embeddings[1]]
    )

    score = similarity[0][0] * 100

    return round(score, 2)
