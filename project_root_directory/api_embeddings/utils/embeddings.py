from langchain_huggingface import HuggingFaceEmbeddings


def generate_embedding(text):
    embedder = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    embedding = embedder.embed_query(text)
    return embedding
