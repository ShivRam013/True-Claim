from graph.graph_search import multi_hop_search
from graph.neo4j_connection import close_connection


try:
    entity = input("\nEnter entity to search: ")

    results = multi_hop_search(entity, hops=3)

    print("\n========== MULTI-HOP GRAPH RESULTS ==========")

    if not results:
        print("No multi-hop knowledge found.")

    else:
        for i, result in enumerate(results, start=1):

            print(f"\nPath {i}")
            print("Hop Count:", result["hop_count"])

            print("\nNodes:")

            for node in result["nodes"]:
                print(
                    f"  {node['name']} "
                    f"({node['type']})"
                )

            print("\nRelationships:")

            for relationship in result["relationships"]:
                print(
                    f"  {relationship['type']}"
                )

                if relationship.get("evidence"):
                    print(
                        f"    Evidence: "
                        f"{relationship['evidence']}"
                    )

finally:
    close_connection()