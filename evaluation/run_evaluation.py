import json

from main import verify_claim
from evaluation.test_dataset import test_cases


def collect_evaluation_data():

    evaluation_data = []

    # Start with one test case to avoid unnecessary API usage.
    for index, test_case in enumerate(test_cases[:1], start=1):

        claim = test_case["claim"]

        print(f"\nEvaluating test case {index}: {claim}")

        result = verify_claim(claim, return_details=True)

        evaluation_data.append({
            "user_input": claim,
            "response": result["response"],
            "retrieved_contexts": result["retrieved_contexts"],
            "reference": test_case["ground_truth"]
        })

    with open("evaluation/evaluation_data.json", "w", encoding="utf-8") as file:
        json.dump(evaluation_data, file, indent=4, ensure_ascii=False)

    print("\nEvaluation data collected successfully.")
    print("Saved to evaluation/evaluation_data.json")


if __name__ == "__main__":
    collect_evaluation_data()