MAX_ITERATIONS = 2


def decision_node(state):

    print("\n========== DECISION NODE ==========")

    iterations = state["iterations"]

    if (
        state["needs_more_evidence"]
        and iterations < MAX_ITERATIONS
    ):
        print("Decision: Investigate Further")

        return {
            "decision": "rewrite_queries",
            "iterations": iterations + 1
        }

    print("Decision: Finalize Investigation")

    return {
        "decision": "finalize"
    }


def route_after_decision(state):

    if state["decision"] == "rewrite_queries":
        return "rewrite_queries"

    return "finalize"