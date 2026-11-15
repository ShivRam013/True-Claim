from graph.entity_extraction import extract_entities_from_claim


claim = input("\nEnter a claim: ")

entities = extract_entities_from_claim(claim)

print("\n========== EXTRACTED ENTITIES ==========")

if not entities:
    print("No useful entities found.")

else:
    for entity in entities:
        print(
            f"Entity: {entity['name']} | "
            f"Type: {entity['type']}"
        )