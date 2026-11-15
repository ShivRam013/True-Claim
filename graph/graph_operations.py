from graph.neo4j_connection import driver


def store_extraction(extraction, chunk_id, chunk_text):
    """
    Store extracted entities, relationships and their
    source information in Neo4j.
    """

    source = extraction["source"]
    page = extraction["page"]

    entities = extraction["entities"]
    relationships = extraction["relationships"]

    # Create a source paper and its original text chunk.
    def create_paper_and_chunk(tx):
        query = """
        MERGE (p:Paper {source: $source})
        MERGE (c:Chunk {chunk_id: $chunk_id})

        SET p.title = $title,
            c.text = $chunk_text,
            c.page = $page,
            c.source = $source

        MERGE (p)-[:HAS_CHUNK]->(c)

        RETURN p, c
        """

        tx.run(
            query,
            source=source,
            title=source.split("\\")[-1],
            chunk_id=chunk_id,
            chunk_text=chunk_text,
            page=page
        )

    # Create entity nodes and link them to their source chunk.
    def create_entities(tx):
        query = """
        MATCH (c:Chunk {chunk_id: $chunk_id})

        UNWIND $entities AS entity

        MERGE (e:Entity {
            name: entity.name,
            type: entity.type
        })

        SET e.description = entity.description

        MERGE (e)-[:MENTIONED_IN]->(c)
        """

        tx.run(
            query,
            chunk_id=chunk_id,
            entities=entities
        )

    # Create relationships between extracted entities.
    def create_relationships(tx):
        query = """
        MATCH (source:Entity {
            name: $source_name,
            type: $source_type
        })

        MATCH (target:Entity {
            name: $target_name,
            type: $target_type
        })

        MERGE (source)-[r:RELATED_TO {
            relationship_type: $relationship_type,
            chunk_id: $chunk_id
        }]->(target)

        SET r.evidence = $evidence,
            r.source = $source
        """

        entity_types = {
            entity["name"]: entity["type"]
            for entity in entities
        }

        for relation in relationships:
            source_name = relation["source"]
            target_name = relation["target"]

            if (
                source_name not in entity_types
                or target_name not in entity_types
            ):
                continue

            tx.run(
                query,
                source_name=source_name,
                source_type=entity_types[source_name],
                target_name=target_name,
                target_type=entity_types[target_name],
                relationship_type=relation["type"],
                evidence=relation["evidence"],
                chunk_id=chunk_id,
                source=source
            )

    with driver.session() as session:
        session.execute_write(create_paper_and_chunk)
        session.execute_write(create_entities)
        session.execute_write(create_relationships)

    print("\nKnowledge successfully stored in Neo4j!")
    print("Paper:", source)
    print("Entities stored:", len(entities))
    print("Relationships stored:", len(relationships))