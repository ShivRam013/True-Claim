from graph.neo4j_connection import driver


def multi_hop_search(entity_name, hops=3):

    if hops < 1 or hops > 3:
        raise ValueError("hops must be between 1 and 3")

    query = f"""
    MATCH (start)
    WHERE start.name IS NOT NULL
      AND toLower(start.name) = toLower($entity_name)

    MATCH path = (start)-[*1..{hops}]-(connected)

    RETURN
        [node IN nodes(path) | {{
            name: coalesce(node.name, node.description),
            type: head(labels(node))
        }}] AS nodes,

        [rel IN relationships(path) | {{
            type: type(rel),
            source: rel.source
        }}] AS relationships,

        length(path) AS hop_count

    LIMIT 30
    """

    with driver.session() as session:
        result = session.run(query, entity_name=entity_name)

        return [
            {
                "nodes": record["nodes"],
                "relationships": record["relationships"],
                "hop_count": record["hop_count"]
            }
            for record in result
        ]