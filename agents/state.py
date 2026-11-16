from typing import Any, Dict, List, TypedDict


class InvestigationState(TypedDict):
    """State shared between all nodes in the LangGraph workflow."""

    # Original user claim
    claim: str

    # Claim decomposition
    subclaims: List[str]

    # Entities extracted from the claim
    entities: List[Dict[str, Any]]

    # Retrieved and analyzed evidence
    evidence: List[Dict[str, Any]]
    supporting_evidence: List[Dict[str, Any]]
    contradicting_evidence: List[Dict[str, Any]]
    inconclusive_evidence: List[Dict[str, Any]]

    # Investigation control
    needs_more_evidence: bool
    iterations: int

    # Search information
    search_queries: List[str]
    new_search_queries: List[str]

    # Detected conflicts between evidence
    evidence_conflicts: List[Dict[str, Any]]

    # Final result
    decision: str
    final_verdict: str
    final_report: Dict[str, Any]