from typing import TypedDict, List, Dict, Any


class InvestigationState(TypedDict):

    # Original claim
    claim: str

    # Claim decomposition
    subclaims: List[str]

    # Extracted entities
    entities: List[Dict[str, Any]]

    # Retrieved evidence
    evidence: List[Dict[str, Any]]

    # Evidence analysis
    supporting_evidence: List[Dict[str, Any]]
    contradicting_evidence: List[Dict[str, Any]]

    # Investigation control
    needs_more_evidence: bool
    iterations: int

    inconclusive_evidence: List[Dict[str, Any]]

    decision: str

    search_queries: List[str]
    new_search_queries: List[str]

    evidence_conflicts: List[Dict[str, Any]]

    # Final result
    final_verdict: str
    final_report: Dict[str, Any]