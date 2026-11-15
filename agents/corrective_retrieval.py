import json

from retrieval.graph_rag import graph_rag_search



def validate_search_query(query):

    if not isinstance(query, str):
        return None

    query = query.strip()

    if not query:
        return None

    if len(query) > 500:
        return None

    return query

def corrective_retrieval_node(state):

    print("\n========== CORRECTIVE RETRIEVAL NODE ==========")

    new_queries = state.get("new_search_queries", [])

    all_evidence = list(state["evidence"])
    all_entities = list(state["entities"])

    seen_evidence = {
        json.dumps(item, sort_keys=True, default=str)
        for item in all_evidence
    }

    for query in new_queries:

        query = validate_search_query(query)

        if query is None:
            print("Skipping invalid search query.")
            continue

        print(f"\nSearching new query: {query}")

        results = graph_rag_search(query)

        # Collect hybrid evidence
        for item in results["hybrid_results"]:

            evidence_item = {
                "type": "hybrid",
                "subclaim": query,
                "text": item["text"],
                "score": item["score"],
                "metadata": item.get("metadata", {})
            }

            key = json.dumps(
                evidence_item,
                sort_keys=True,
                default=str
            )

            if key not in seen_evidence:
                all_evidence.append(evidence_item)
                seen_evidence.add(key)

        # Collect graph evidence
        for item in results["graph_results"]:

            evidence_item = {
                "type": "graph",
                "subclaim": query,
                "path": item["path"],
                "search_entity": item["search_entity"]
            }

            key = json.dumps(
                evidence_item,
                sort_keys=True,
                default=str
            )

            if key not in seen_evidence:
                all_evidence.append(evidence_item)
                seen_evidence.add(key)

        # Collect entities
        for entity in results["entities"]:
            if entity not in all_entities:
                all_entities.append(entity)

    print("\nCorrective retrieval completed!")
    print("Total evidence:", len(all_evidence))

    return {
        "evidence": all_evidence,
        "entities": all_entities,
        "new_search_queries": []
    }