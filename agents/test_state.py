from agents.state import InvestigationState

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
    "search_queries": [],
    "final_verdict": ""
    
}

print("Investigation State Created Successfully!")

print("\nClaim:", state["claim"])
print("Iterations:", state["iterations"])
print("Needs More Evidence:", state["needs_more_evidence"])