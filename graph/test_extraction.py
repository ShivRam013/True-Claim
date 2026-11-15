import json
from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from graph.extraction import extract_graph_data


# Find a research paper
pdf_files = list(Path("data/papers").glob("*.pdf"))

if not pdf_files:
    raise FileNotFoundError("No PDF found inside data/papers")

pdf_path = pdf_files[0]

print("Loading:", pdf_path.name)

# Load PDF
loader = PyPDFLoader(str(pdf_path))
documents = loader.load()

# Split into chunks
splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)

chunks = splitter.split_documents(documents)

if not chunks:
    raise ValueError("No text chunks extracted from the PDF")

print("Total chunks:", len(chunks))

# Find a chunk containing meaningful project content
for i, chunk in enumerate(chunks):
    if len(chunk.page_content.strip()) > 300:
        print(f"\nTesting chunk: {i}")
        print("\n========== CHUNK TEXT ==========")
        print(chunk.page_content)

        result = extract_graph_data(chunk)

        print("\n========== EXTRACTION RESULT ==========")
        print(json.dumps(result, indent=4, ensure_ascii=False))
        break

print("\n========== EXTRACTION RESULT ==========")
print(json.dumps(result, indent=4, ensure_ascii=False))