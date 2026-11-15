from agents.state import InvestigationState
from agents.retrieval_node import evidence_retrieval_node
from agents.evidence_analysis import evidence_analysis_node

from graph.neo4j_connection import close_connection


state: InvestigationState = {
    "claim": "LoRA reduces LLM fine-tuning costs.",
    "subclaims": [],
    "entities": [],
    "evidence": [],
    "supporting_evidence": [],
    "contradicting_evidence": [],
    "inconclusive_evidence": [],
    "needs_more_evidence": True,
    "iterations": 0,
    "final_verdict": ""
}

try:
    # Retrieve evidence
    state.update(evidence_retrieval_node(state))

    # Analyze evidence
    state.update(evidence_analysis_node(state))

    print("\n========== ANALYSIS RESULTS ==========")

    print(
        "Supporting:",
        len(state["supporting_evidence"])
    )

    print(
        "Contradicting:",
        len(state["contradicting_evidence"])
    )

    print(
        "Inconclusive:",
        len(state["inconclusive_evidence"])
    )

    print(
        "Needs More Evidence:",
        state["needs_more_evidence"]
    )

finally:
    close_connection()