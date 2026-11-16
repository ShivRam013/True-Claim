import re

from retrieval.claim_decomposition import decompose_claim
from retrieval.graph_rag import graph_rag_search


def extract_subclaims(decomposition):
    """Convert the LLM decomposition into a clean list of subclaims."""

    subclaims = []

    for line in decomposition.splitlines():
        # Remove bullets such as "-", "*", "1.", and "1)"
        line = re.sub(r"^\s*(?:[-*]|\d+[.)])\s*", "", line).strip()

        if line:
            subclaims.append(line)

    return subclaims


def evidence_retrieval_node(state):
    """Decompose the claim and retrieve evidence using GraphRAG."""

    claim = state["claim"]

    print("\n========== EVIDENCE RETRIEVAL NODE ==========")

    # 1. Decompose the original claim into smaller subclaims
    print("\nDecomposing claim...")

    decomposition = decompose_claim(claim)
    subclaims = extract_subclaims(decomposition)

    # Use the original claim if decomposition produces nothing
    if not subclaims:
        subclaims = [claim]

    # Store evidence and entities from all subclaims
    all_evidence = []
    all_entities = []

    # 2. Search for evidence for each subclaim
    for i, subclaim in enumerate(subclaims, start=1):
        print(f"\nInvestigating subclaim {i}: {subclaim}")

        results = graph_rag_search(subclaim)

        # Collect unique entities
        for entity in results["entities"]:
            if entity not in all_entities:
                all_entities.append(entity)

        # Collect Hybrid RAG results
        for item in results["hybrid_results"]:
            all_evidence.append({
                "type": "hybrid",
                "subclaim": subclaim,
                "text": item["text"],
                "score": item["score"],
                "metadata": item.get("metadata", {}),
            })

        # Collect Multi-Hop GraphRAG results
        for item in results["graph_results"]:
            all_evidence.append({
                "type": "graph",
                "subclaim": subclaim,
                "path": item["path"],
                "search_entity": item["search_entity"],
            })

    print("\nEvidence retrieval completed!")
    print("Subclaims:", len(subclaims))
    print("Entities:", len(all_entities))
    print("Evidence items:", len(all_evidence))

    # 3. Return data to the LangGraph state
    return {
        "subclaims": subclaims,
        "entities": all_entities,
        "evidence": all_evidence,
    }