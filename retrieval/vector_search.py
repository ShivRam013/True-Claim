from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings


# Initialize the embedding model
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# Connect to the existing Chroma vector database
db = Chroma(
    collection_name="true_claim_papers",
    embedding_function=embeddings,
    persist_directory="chroma_db",
)


def retrieve_evidence(claim, k=5):
    """Retrieve the most relevant documents using vector similarity."""

    return db.similarity_search(claim, k=k)