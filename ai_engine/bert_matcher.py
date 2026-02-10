from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


# Load AI model once
model = SentenceTransformer('paraphrase-MiniLM-L3-v2')


def semantic_similarity(resume_text, job_text):

    # Convert text into embeddings
    embeddings = model.encode([resume_text, job_text])

    # Calculate similarity
    similarity = cosine_similarity(
        [embeddings[0]],
        [embeddings[1]]
    )

    # Convert to percentage
    score = similarity[0][0] * 100

    return round(score, 2)
