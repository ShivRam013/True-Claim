import re

from retrieval.claim_decomposition import decompose_claim
from retrieval.graph_rag import graph_rag_search


def extract_subclaims(decomposition):
    subclaims = []

    for line in decomposition.splitlines():
        line = re.sub(
            r"^\s*(?:[-*]|\d+[.)])\s*",
            "",
            line
        ).strip()

        if line:
            subclaims.append(line)

    return subclaims


def evidence_retrieval_node(state):

    claim = state["claim"]

    print("\n========== EVIDENCE RETRIEVAL NODE ==========")

    # 1. Decompose the original claim
    print("\nDecomposing claim...")

    decomposition = decompose_claim(claim)
    subclaims = extract_subclaims(decomposition)

    if not subclaims:
        subclaims = [claim]

    # 2. Retrieve evidence for every subclaim
    all_evidence = []
    all_entities = []

    for i, subclaim in enumerate(subclaims, start=1):

        print(f"\nInvestigating subclaim {i}: {subclaim}")

        results = graph_rag_search(subclaim)

        # Collect entities
        for entity in results["entities"]:
            if entity not in all_entities:
                all_entities.append(entity)

        # Collect Hybrid RAG evidence
        for item in results["hybrid_results"]:

            all_evidence.append({
                "type": "hybrid",
                "subclaim": subclaim,
                "text": item["text"],
                "score": item["score"],
                "metadata": item.get("metadata", {})
            })

        # Collect Multi-Hop GraphRAG evidence
        for item in results["graph_results"]:

            all_evidence.append({
                "type": "graph",
                "subclaim": subclaim,
                "path": item["path"],
                "search_entity": item["search_entity"]
            })

    print("\nEvidence retrieval completed!")
    print("Subclaims:", len(subclaims))
    print("Entities:", len(all_entities))
    print("Evidence items:", len(all_evidence))

    # 3. Update LangGraph state
    return {
        "subclaims": subclaims,
        "entities": all_entities,
        "evidence": all_evidence
    }