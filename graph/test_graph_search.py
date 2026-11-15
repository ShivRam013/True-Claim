from graph.graph_search import search_graph
from graph.neo4j_connection import close_connection


try:
    entity = input("\nEnter entity to search: ")

    results = search_graph(entity)

    print("\n========== GRAPH SEARCH RESULTS ==========")

    if not results:
        print("No connected knowledge found.")

    else:
        for i, result in enumerate(results, start=1):

            print(f"\nResult {i}")
            print("Entity:", result["entity"])
            print("Type:", result["entity_type"])
            print("Connected:", result["connected_entity"])
            print("Connected Type:", result["connected_type"])
            print("Relationships:", result["relationships"])

finally:
    close_connection()