from agents.workflow import investigation_graph
from graph.neo4j_connection import close_connection
from utils.security.middleware import pii_middleware


original_claim = "The Student Placement Prediction System dataset contains only 500 student records."
sanitized_claim = pii_middleware(original_claim)

initial_state = {
    "claim": sanitized_claim,
    "subclaims": [],
    "entities": [],
    "evidence": [],
    "supporting_evidence": [],
    "contradicting_evidence": [],
    "inconclusive_evidence": [],
    "needs_more_evidence": True,
    "iterations": 0,
    "decision": "",
    "search_queries": [],
    "new_search_queries": [],
    "final_report": {},
    "final_verdict": ""
}

try:

    print("\n========== TRUE CLAIM INVESTIGATION ==========")

    result = investigation_graph.invoke(initial_state)

    print("Claim:", result["claim"])

    print("Verdict:", result["final_verdict"])

    report = result["final_report"]

    print("\nReasoning:")
    print(report["reasoning"])

    print("\nSupporting Evidence IDs:")
    print(report["supporting_evidence"])

    print("\nContradicting Evidence IDs:")
    print(report["contradicting_evidence"])

    print("\nLimitations:")
    for limitation in report["limitations"]:
        print("-", limitation)

    print("\nConfidence:", report["confidence"])

    print(result["final_report"].get("citations",{}))

finally:
    close_connection()
