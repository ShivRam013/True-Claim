import argparse
import json
import os
from pathlib import Path

from dotenv import load_dotenv
from openai import AsyncOpenAI
import instructor

from main import verify_claim

from ragas.llms import llm_factory
from ragas.metrics.collections import (
    Faithfulness,
    AnswerRelevancy,
    ContextPrecision,
    ContextRecall
)
from ragas.embeddings.base import embedding_factory


load_dotenv()

INPUT_PATH = Path("evaluation/ragas_input.json")
RESULTS_PATH = Path("evaluation/ragas_metric_results.json")

CLAIM = (
    "LoRA reduces the number of trainable parameters "
    "compared with full fine-tuning."
)

REFERENCE = (
    "LoRA freezes the pretrained model weights and introduces "
    "trainable low-rank matrices into selected model layers. "
    "During fine-tuning, only these low-rank parameters are "
    "updated instead of updating all pretrained model "
    "parameters. This substantially reduces the number of "
    "trainable parameters compared with full fine-tuning."
)


def prepare_data():
    """Run True Claim once and save its output for evaluation."""

    print("\n========== PREPARING EVALUATION DATA ==========")

    result = verify_claim(
        CLAIM,
        return_details=True
    )

    response = result["response"]
    retrieved_contexts = result["retrieved_contexts"]

    data = {
        "claim": CLAIM,
        "reference": REFERENCE,
        "response": response[:3000],
        "retrieved_contexts": [
            context[:600]
            for context in retrieved_contexts
        ]
    }

    INPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    with open(INPUT_PATH, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

    print("Response length:", len(response))
    print("Retrieved contexts:", len(retrieved_contexts))
    print("Evaluation data saved to:", INPUT_PATH)


def load_data():
    if not INPUT_PATH.exists():
        raise FileNotFoundError(
            "Evaluation data not found. Run prepare first."
        )

    with open(INPUT_PATH, "r", encoding="utf-8") as file:
        return json.load(file)


def create_evaluator():
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise ValueError("GROQ_API_KEY is missing in .env")

    client = AsyncOpenAI(
        api_key=api_key,
        base_url="https://api.groq.com/openai/v1"
    )

    return llm_factory(
        "openai/gpt-oss-120b",
        provider="openai",
        client=client,
        mode=instructor.Mode.MD_JSON,
        max_tokens=8192
    )


def save_score(metric_name, score, data):
    """Save a completed metric immediately."""

    if RESULTS_PATH.exists():
        with open(RESULTS_PATH, "r", encoding="utf-8") as file:
            results = json.load(file)
    else:
        results = {}

    results.update({
        "claim": data["claim"],
        "reference": data["reference"],
        metric_name: score
    })

    RESULTS_PATH.parent.mkdir(parents=True, exist_ok=True)

    with open(RESULTS_PATH, "w", encoding="utf-8") as file:
        json.dump(results, file, indent=4, ensure_ascii=False)

    print(f"{metric_name}: {score}")
    print("Saved to:", RESULTS_PATH)


def evaluate(metric_name):
    data = load_data()

    print(f"\n========== {metric_name.upper()} EVALUATION ==========")

    evaluator_llm = create_evaluator()

    if metric_name == "faithfulness":
        metric = Faithfulness(llm=evaluator_llm)

        score = metric.score(
            user_input=data["claim"],
            response=data["response"],
            retrieved_contexts=data["retrieved_contexts"]
        )

    elif metric_name == "relevancy":
        evaluator_embeddings = embedding_factory(
            provider="huggingface",
            model="sentence-transformers/all-MiniLM-L6-v2"
        )

        metric = AnswerRelevancy(
            llm=evaluator_llm,
            embeddings=evaluator_embeddings
        )

        score = metric.score(
            user_input=data["claim"],
            response=data["response"]
        )

    elif metric_name == "precision":
        metric = ContextPrecision(llm=evaluator_llm)

        score = metric.score(
            user_input=data["claim"],
            reference=data["reference"],
            retrieved_contexts=data["retrieved_contexts"]
        )

    elif metric_name == "recall":
        metric = ContextRecall(llm=evaluator_llm)

        score = metric.score(
            user_input=data["claim"],
            reference=data["reference"],
            retrieved_contexts=data["retrieved_contexts"]
        )

    save_score(
        f"{metric_name}_score",
        score.value,
        data
    )


def main():
    parser = argparse.ArgumentParser(
        description="True Claim RAGAS evaluation"
    )

    parser.add_argument(
        "action",
        choices=[
            "prepare",
            "faithfulness",
            "relevancy",
            "precision",
            "recall"
        ],
        help="Choose data preparation or one evaluation metric"
    )

    args = parser.parse_args()

    if args.action == "prepare":
        prepare_data()
    else:
        evaluate(args.action)


if __name__ == "__main__":
    main()