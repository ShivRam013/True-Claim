from langgraph.graph import END, START, StateGraph

from agents.corrective_retrieval import corrective_retrieval_node
from agents.decision_node import decision_node, route_after_decision
from agents.evidence_analysis import evidence_analysis_node
from agents.evidence_relevance import evidence_relevance_node
from agents.query_rewriting import query_rewriting_node
from agents.retrieval_node import evidence_retrieval_node
from agents.state import InvestigationState
from agents.verdict_node import verdict_generation_node


def build_investigation_graph():
    """Build and compile the True Claim investigation workflow."""

    workflow = StateGraph(InvestigationState)

    # Register investigation nodes
    workflow.add_node("retrieve", evidence_retrieval_node)
    workflow.add_node("relevance", evidence_relevance_node)
    workflow.add_node("analyze", evidence_analysis_node)
    workflow.add_node("decide", decision_node)
    workflow.add_node("rewrite", query_rewriting_node)
    workflow.add_node("corrective_retrieve", corrective_retrieval_node)
    workflow.add_node("finalize", verdict_generation_node)

    # Main investigation flow
    workflow.add_edge(START, "retrieve")
    workflow.add_edge("retrieve", "relevance")
    workflow.add_edge("relevance", "analyze")
    workflow.add_edge("analyze", "decide")

    # Decide whether more evidence is needed
    workflow.add_conditional_edges(
        "decide",
        route_after_decision,
        {
            "rewrite_queries": "rewrite",
            "finalize": "finalize",
        },
    )

    # Corrective retrieval loop
    workflow.add_edge("rewrite", "corrective_retrieve")
    workflow.add_edge("corrective_retrieve", "analyze")

    # Finish the investigation
    workflow.add_edge("finalize", END)

    return workflow.compile()


investigation_graph = build_investigation_graph()