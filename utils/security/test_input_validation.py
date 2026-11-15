from utils.security.input_validation import validate_claim


test_claims = [
    "Does LoRA reduce LLM fine-tuning costs?",
    33333,
    "     ",
    "A" * 2001,
]

for claim in test_claims:

    try:
        result = validate_claim(claim)
        print("VALID:", result)

    except ValueError as error:
        print("INVALID:", error)