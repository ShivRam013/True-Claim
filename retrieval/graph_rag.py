from retrieval.hybrid_search import hybrid_search
from graph.entity_extraction import extract_entities_from_claim
from graph.graph_search import multi_hop_search


def graph_rag_search(claim, top_k=5):
    """Retrieve evidence using Hybrid RAG and multi-hop GraphRAG."""

    # 1. Retrieve relevant research documents
    print("\nPerforming Hybrid Search...")

    hybrid_results = hybrid_search(claim, top_k=top_k)

    # 2. Extract entities from the claim
    print("\nExtracting claim entities...")

    entities = extract_entities_from_claim(claim)

    # 3. Search Neo4j for connected knowledge
    print("\nPerforming Multi-Hop Graph Search...")

    graph_results = []

    for entity in entities:
        results = multi_hop_search(
            entity["name"],
            hops=3,
        )

        for result in results:
            graph_results.append({
                "search_entity": entity["name"],
                "path": result,
            })

    # 4. Return combined retrieval results
    return {
        "claim": claim,
        "entities": entities,
        "hybrid_results": hybrid_results,
        "graph_results": graph_results,
    }