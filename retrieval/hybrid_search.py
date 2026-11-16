from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from rank_bm25 import BM25Okapi
from sentence_transformers import CrossEncoder


# Initialize the embedding model and Chroma vector database
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

db = Chroma(
    collection_name="true_claim_papers",
    embedding_function=embeddings,
    persist_directory="chroma_db",
)


# Load stored documents and metadata for BM25 search
data = db.get(include=["documents", "metadatas"])

documents = data["documents"]
metadatas = data["metadatas"]


# Initialize BM25 keyword search
tokenized_documents = [
    document.lower().split()
    for document in documents
]

bm25 = BM25Okapi(tokenized_documents)


# Initialize the CrossEncoder reranking model
reranker = CrossEncoder(
    "cross-encoder/ms-marco-MiniLM-L-6-v2"
)


def hybrid_search(claim, top_k=10):
    """Retrieve documents using vector search and BM25, then rerank them."""

    # 1. Retrieve documents using semantic vector search
    vector_results = db.similarity_search(claim, k=top_k)

    vector_documents = [
        {
            "text": doc.page_content,
            "metadata": doc.metadata,
        }
        for doc in vector_results
    ]

    # 2. Retrieve documents using keyword search
    tokenized_claim = claim.lower().split()

    bm25_results = bm25.get_top_n(
        tokenized_claim,
        documents,
        n=top_k,
    )

    bm25_documents = []

    for document in bm25_results:
        index = documents.index(document)

        bm25_documents.append({
            "text": document,
            "metadata": metadatas[index],
        })

    # 3. Combine results and remove duplicate text
    combined_documents = []
    seen = set()

    for item in vector_documents + bm25_documents:
        text = item["text"]

        if text not in seen:
            seen.add(text)
            combined_documents.append(item)

    # 4. Rerank documents based on their relevance to the claim
    pairs = [
        [claim, item["text"]]
        for item in combined_documents
    ]

    scores = reranker.predict(pairs)

    ranked_results = sorted(
        zip(combined_documents, scores),
        key=lambda item: item[1],
        reverse=True,
    )

    # 5. Return the five highest-ranked results
    return [
        {
            "text": item["text"],
            "score": float(score),
            "metadata": item["metadata"],
        }
        for item, score in ranked_results[:5]
    ]