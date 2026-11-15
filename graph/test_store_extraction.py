import json
from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from graph.extraction import extract_graph_data
from graph.graph_operations import store_extraction
from graph.neo4j_connection import close_connection


try:
    pdf_files = list(Path("data/papers").glob("*.pdf"))

    if not pdf_files:
        raise FileNotFoundError("No PDF found in data/papers")

    pdf_path = pdf_files[0]

    print("Loading:", pdf_path.name)

    loader = PyPDFLoader(str(pdf_path))
    documents = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    chunks = splitter.split_documents(documents)

    print("Total chunks:", len(chunks))

    # Select a meaningful chunk.
    selected_chunk = None
    selected_index = None

    for i, chunk in enumerate(chunks):
        if len(chunk.page_content.strip()) > 300:
            selected_chunk = chunk
            selected_index = i
            break

    if selected_chunk is None:
        raise ValueError("No suitable chunk found")

    print("\nExtracting knowledge...")

    extraction = extract_graph_data(selected_chunk)

    print("\nExtraction result:")
    print(json.dumps(extraction, indent=4))

    # Generate a unique ID for this source chunk.
    page = selected_chunk.metadata.get("page", "unknown")

    chunk_id = (
        f"{pdf_path.name}:page-{page}:chunk-{selected_index}"
    )

    print("\nStoring in Neo4j...")

    store_extraction(
        extraction=extraction,
        chunk_id=chunk_id,
        chunk_text=selected_chunk.page_content
    )

finally:
    close_connection()