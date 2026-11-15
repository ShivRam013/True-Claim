from agents.query_rewriting import query_rewriting_node


state = {
    "claim": "LoRA reduces LLM fine-tuning costs without reducing performance.",

    "supporting_evidence": [
        {
            "type": "hybrid",
            "text": "LoRA reduces the number of trainable parameters."
        }
    ],

    "contradicting_evidence": [],

    "inconclusive_evidence": [
        {
            "type": "hybrid",
            "text": "The evidence does not establish benchmark performance."
        }
    ],

    "search_queries": []
}


result = query_rewriting_node(state)

print("\n========== QUERY REWRITING RESULTS ==========")

for query in result["search_queries"]:
    print("-", query)