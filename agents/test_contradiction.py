from agents.evidence_analysis import evidence_analysis_node


# Synthetic evidence for testing only.
# These are NOT actual findings from your project report.

test_state = {
    "claim": (
        "Using multiple machine learning algorithms improves "
        "the accuracy of student placement prediction."
    ),

    "evidence": [
        {
            "type": "hybrid",
            "subclaim": (
                "Machine learning algorithms improve "
                "student placement prediction."
            ),
            "text": (
                "Synthetic Finding A: In a hypothetical student "
                "placement experiment, a Random Forest model achieved "
                "88% accuracy, while the baseline model achieved 78%. "
                "This suggests that machine learning improved "
                "placement prediction performance."
            ),
            "score": 1.0,
            "metadata": {
                "source": "synthetic_placement_study_A.pdf",
                "page": 5
            }
        },
        {
            "type": "hybrid",
            "subclaim": (
                "Machine learning algorithms do not always "
                "improve student placement prediction."
            ),
            "text": (
                "Synthetic Finding B: In a hypothetical student "
                "placement experiment using a comparable dataset "
                "and evaluation setup, a Random Forest model "
                "achieved 76% accuracy, while the baseline model "
                "achieved 82%. This suggests that the machine "
                "learning model performed worse than the baseline."
            ),
            "score": 0.9,
            "metadata": {
                "source": "synthetic_placement_study_B.pdf",
                "page": 8
            }
        }
    ]
}


result = evidence_analysis_node(test_state)


print("\n========== STUDENT PLACEMENT CONTRADICTION TEST ==========")

print("\nSupporting evidence:")
for item in result["supporting_evidence"]:
    print("-", item["text"][:200])

print("\nContradicting evidence:")
for item in result["contradicting_evidence"]:
    print("-", item["text"][:200])

print("\nInconclusive evidence:")
for item in result["inconclusive_evidence"]:
    print("-", item["text"][:200])

print("\nDetected conflicts:")
for conflict in result["evidence_conflicts"]:
    print("Evidence IDs:", conflict["evidence_ids"])
    print("Explanation:", conflict["explanation"])

print("\nNeeds more evidence:", result["needs_more_evidence"])