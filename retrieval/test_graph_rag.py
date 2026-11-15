from retrieval.graph_rag import graph_rag_search
from graph.neo4j_connection import close_connection


try:
    claim = input("\nEnter a scientific claim: ")

    results = graph_rag_search(claim)

    print("\n========== EXTRACTED ENTITIES ==========")

    for entity in results["entities"]:
        print(entity)

    print("\n========== HYBRID RAG EVIDENCE ==========")

    for i, result in enumerate(
        results["hybrid_results"], start=1
    ):
        print(f"\nEvidence {i}")
        print("Score:", result["score"])
        print("Text:", result["text"])

    print("\n========== MULTI-HOP GRAPH EVIDENCE ==========")

    if not results["graph_results"]:
        print("No connected graph evidence found.")

    for i, result in enumerate(
        results["graph_results"], start=1
    ):
        path = result["path"]

        print(f"\nGraph Path {i}")
        print("Search Entity:", result["search_entity"])
        print("Hop Count:", path["hop_count"])

        print("Nodes:")
        for node in path["nodes"]:
            print(node)

        print("Relationships:")
        for relationship in path["relationships"]:
            print(relationship)

finally:
    close_connection()