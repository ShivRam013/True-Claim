import json
from dotenv import load_dotenv

from agents.workflow import investigation_graph
from graph.neo4j_connection import close_connection

from utils.security.middleware import pii_middleware
from utils.security.input_validation import validate_claim
from utils.security.output_validation import validate_output

load_dotenv()


def verify_claim(claim):

    print("\n========== TRUE CLAIM INVESTIGATION ==========")

    # Step 1: Validate input
    validated_claim = validate_claim(claim)

    # Step 2: Anonymize PII
    sanitized_claim = pii_middleware(validated_claim)

    # Step 3: Initialize LangGraph state
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
        "evidence_conflicts": [],
        "final_report": {},
        "final_verdict": ""
    }

    # Step 4: Run LangGraph investigation
    result = investigation_graph.invoke(initial_state)

    # Step 5: Extract final report
    report = result["final_report"]

    # Step 6: Validate output
    report_json = json.dumps(report, indent=4)
    validated_report = validate_output(report_json)

    return result["final_verdict"], validated_report


if __name__ == "__main__":

    try:

        claim = input("\nEnter your scientific claim: ")

        verdict, report_json = verify_claim(claim)

        report = json.loads(report_json)

        print("\n========== TRUE CLAIM REPORT ==========")

        print("\nClaim:")
        print(claim)

        print("\nFinal Verdict:")
        print(verdict)

        print("\nReasoning:")
        print(report.get("reasoning", ""))

        print("\nSupporting Evidence IDs:")
        print(report.get("supporting_evidence", []))

        print("\nContradicting Evidence IDs:")
        print(report.get("contradicting_evidence", []))

        print("\nLimitations:")
        for limitation in report.get("limitations", []):
            print("-", limitation)

        print("\nConfidence:")
        print(report.get("confidence", "Low"))

        print("\nCitations:")
        print(json.dumps(report.get("citations", {}), indent=4))

    finally:
        close_connection()