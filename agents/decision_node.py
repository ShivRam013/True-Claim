MAX_ITERATIONS = 2


def decision_node(state):
    """Decide whether to retrieve more evidence or finalize the investigation."""

    print("\n========== DECISION NODE ==========")

    iterations = state["iterations"]

    # Continue investigation if more evidence is needed
    # and the maximum number of iterations has not been reached.
    if state["needs_more_evidence"] and iterations < MAX_ITERATIONS:
        print("Decision: Investigate Further")

        return {
            "decision": "rewrite_queries",
            "iterations": iterations + 1,
        }

    # Otherwise, finish the investigation
    print("Decision: Finalize Investigation")

    return {
        "decision": "finalize",
    }


def route_after_decision(state):
    """Route the workflow based on the decision."""

    if state["decision"] == "rewrite_queries":
        return "rewrite_queries"

    return "finalize"