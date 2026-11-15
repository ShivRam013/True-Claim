from agents.decision_node import (
    decision_node,
    route_after_decision
)

state = {
    "iterations": 0,
    "needs_more_evidence": True,
    "supporting_evidence": [],
    "contradicting_evidence": [],
    "inconclusive_evidence": [],
    "decision": ""
}

for attempt in range(4):

    result = decision_node(state)
    state.update(result)

    route = route_after_decision(state)

    print("Next Route:", route)

    if route == "finalize":
        break

print("\nFinal Iterations:", state["iterations"])
print("Final Decision:", state["decision"])
