from agents.state import InvestigationState
from agents.retrieval_node import evidence_retrieval_node
from graph.neo4j_connection import close_connection


state: InvestigationState = {
    "claim": "The student placement prediction project aims to predict whether a student will be placed or not using a dataset of 100,000 students.",
    "subclaims": [],
    "entities": [],
    "evidence": [],
    "supporting_evidence": [],
    "contradicting_evidence": [],
    "needs_more_evidence": True,
    "iterations": 0,
    "inconclusive_evidence": [],
    "final_verdict": ""
}

try:
    updated_state = evidence_retrieval_node(state)

    state.update(updated_state)

    print("\n========== RETRIEVAL SUMMARY ==========")

    print("Subclaims:", state["subclaims"])
    print("Entities:", state["entities"])
    print("Total Evidence:", len(state["evidence"]))

    for i, evidence in enumerate(state["evidence"], start=1):
        print(f"\nEvidence {i}")
        print("Type:", evidence["type"])
        print("Subclaim:", evidence["subclaim"])

        if evidence["type"] == "hybrid":
            print("Text:", evidence["text"][:300])

        else:
            print("Graph Path:", evidence["path"])

finally:
    close_connection()