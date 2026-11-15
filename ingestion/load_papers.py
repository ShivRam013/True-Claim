from pathlib import Path
import hashlib

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma


PAPER_DIR = Path("data/papers")
DB_DIR = "chroma_db"

# 1. Load PDFs
documents = []

for pdf in PAPER_DIR.glob("*.pdf"):
    loader = PyPDFLoader(str(pdf))
    pages = loader.load()

    for page in pages:
        page.metadata["source"] = pdf.name

    documents.extend(pages)

if not documents:
    raise ValueError("No PDF files found in data/papers/")

print(f"Loaded {len(documents)} pages")

# 2. Chunking
splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)

chunks = splitter.split_documents(documents)

print(f"Created {len(chunks)} chunks")

# 3. Embeddings
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# 4. Store in ChromaDB
db = Chroma(
    collection_name="true_claim_papers",
    embedding_function=embeddings,
    persist_directory=DB_DIR
)

# Generate stable IDs to avoid duplicate chunks on reruns
ids = []

for chunk in chunks:
    unique_text = (
        f"{chunk.metadata['source']}"
        f"{chunk.metadata['page']}"
        f"{chunk.page_content}"
    )

    ids.append(
        hashlib.sha256(unique_text.encode()).hexdigest()
    )

db.add_documents(
    documents=chunks,
    ids=ids
)

print("Research papers successfully stored in ChromaDB!")