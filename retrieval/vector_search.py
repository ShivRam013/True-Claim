from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma


embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

db = Chroma(
    collection_name="true_claim_papers",
    embedding_function=embeddings,
    persist_directory="chroma_db"
)


def retrieve_evidence(claim, k=5):

    results = db.similarity_search(
        claim,
        k=k
    )

    return results