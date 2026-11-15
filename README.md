# True Claim — Agentic AI Scientific Claim Verification

True Claim is an AI-powered scientific claim verification system that investigates factual and scientific claims using research documents, advanced Retrieval-Augmented Generation (RAG), knowledge graphs, and agentic AI workflows.

Instead of relying only on an LLM's internal knowledge, True Claim retrieves relevant evidence, analyzes supporting and contradicting information, and generates an evidence-based verdict with source citations.

## Key Features

- **Claim Decomposition:** Breaks complex claims into smaller, verifiable subclaims.
- **Advanced RAG:** Combines semantic vector search and keyword-based retrieval.
- **Reranking:** Improves evidence selection using a Cross-Encoder.
- **GraphRAG:** Uses Neo4j to extract entities and explore relationships through multi-hop graph search.
- **Agentic Investigation:** Uses LangGraph to coordinate retrieval, evidence analysis, corrective retrieval, and verdict generation.
- **Contradiction Detection:** Identifies evidence that supports or contradicts a claim.
- **Corrective Retrieval:** Rewrites search queries and retrieves additional evidence when necessary.
- **Security:** Includes input validation, PII handling, and output validation.
- **LLM Gateway:** Uses LiteLLM for centralized LLM interaction.
- **Evaluation and Monitoring:** Uses RAGAS for retrieval and response evaluation and LangSmith for tracing and token tracking.

## Possible Verdicts

| Verdict | Meaning |
|---|---|
| Supported | Available evidence supports the claim. |
| Contradicted | Available evidence conflicts with the claim. |
| Insufficient | Available evidence is not sufficient to establish either conclusion. |

## Technology Stack

| Category | Technologies |
|---|---|
| Language | Python |
| LLM Integration | LiteLLM, Groq |
| AI Framework | LangChain |
| Agentic Workflow | LangGraph |
| Vector Database | ChromaDB |
| Knowledge Graph | Neo4j |
| Embeddings | Hugging Face Sentence Transformers |
| Retrieval | BM25, Vector Search, Hybrid Search |
| Reranking | Cross-Encoder |
| Evaluation | RAGAS |
| Monitoring | LangSmith |
| PDF Processing | PyPDF |
| Environment Management | uv |

## System Architecture

1. **Input Processing:** Validates the submitted claim and applies PII handling.
2. **Claim Decomposition:** Breaks the claim into smaller subclaims.
3. **Evidence Retrieval:** Retrieves relevant information using Hybrid RAG and GraphRAG.
4. **Evidence Relevance:** Filters retrieved evidence based on relevance.
5. **Evidence Analysis:** Classifies evidence as supporting, contradicting, or inconclusive.
6. **Investigation Decision:** Determines whether additional evidence is required.
7. **Corrective Retrieval:** Rewrites queries and retrieves additional evidence when necessary.
8. **Verdict Generation:** Generates the final verdict, reasoning, confidence, and citations.
9. **Output Validation:** Validates the generated report.

## Project Structure

```text
True-Claim/
│
├── agents/
│   ├── corrective_retrieval.py
│   ├── decision_node.py
│   ├── evidence_analysis.py
│   ├── evidence_relevance.py
│   ├── query_rewriting.py
│   ├── retrieval_node.py
│   ├── state.py
│   ├── verdict_node.py
│   └── workflow.py
│
├── data/
│   └── research documents
│
├── evaluation/
│   ├── ragas_evaluation.py
│   ├── run_evaluation.py
│   └── evaluation datasets and results
│
├── graph/
│   ├── entity_extraction.py
│   ├── extraction.py
│   ├── graph_operations.py
│   ├── graph_search.py
│   └── neo4j_connection.py
│
├── ingestion/
│   └── load_paper.py
│
├── retrieval/
│   ├── claim_decomposition.py
│   ├── graph_rag.py
│   ├── hybrid_search.py
│   └── vector_search.py
│
├── utils/
│   ├── config.py
│   ├── llm_gateway.py
│   └── security/
│
├── chroma_db/
├── main.py
├── pyproject.toml
├── requirements.txt
├── uv.lock
└── README.md
```

## Installation and Setup

### 1. Clone the repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd True-Claim
```

### 2. Install dependencies

Install uv if it is not already installed, then run:

```bash
uv sync
```

### 3. Configure environment variables

Create a ".env" file in the project root:

GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=openai/gpt-oss-120b

NEO4J_URI=your_neo4j_uri
NEO4J_USERNAME=your_neo4j_username
NEO4J_PASSWORD=your_neo4j_password

- "GROQ_API_KEY": Your Groq API key.
- "GROQ_MODEL": The LLM model used by the application.

The default model is "openai/gpt-oss-120b".

Keep your API keys private. Never upload your ".env" file to GitHub.

Ensure your Neo4j database is running and configure the connection settings required by "graph/neo4j_connection.py" in your ".env" file.

### 4. Run the application

```bash
uv run python main.py
```

### 5. Enter a claim

When prompted, enter a scientific or factual claim to begin the investigation.

## Evaluation

True Claim uses RAGAS to evaluate retrieval and response quality.

The evaluation includes:

- Faithfulness
- Answer Relevancy
- Context Precision
- Context Recall

LangSmith is used for workflow tracing and token tracking.

## Current Project Status

- Advanced RAG pipeline implemented.
- Hybrid retrieval and reranking implemented.
- Neo4j knowledge graph and multi-hop retrieval implemented.
- LangGraph investigation workflow implemented.
- Corrective retrieval and contradiction detection implemented.
- Security middleware and output validation implemented.
- RAGAS evaluation integrated.
- LangSmith tracing integrated.
- Main application entry point integrated with LangGraph.
- End-to-end verdict tests completed for Supported, Contradicted, and Insufficient claims.

## Future Improvements

- Develop a user-friendly frontend.
- Build a backend API.
- Deploy the application.
- Improve evidence presentation and user interaction.

## Disclaimer

True Claim provides evidence-based claim analysis using the documents and information available in its knowledge base. Its verdicts should not be treated as absolute proof or a substitute for independent scientific verification.
