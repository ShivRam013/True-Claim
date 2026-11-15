from utils.security.output_validation import validate_output


test_outputs = [
    "Verdict: Supported. LoRA reduces fine-tuning costs.",
    "",
    "     ",
    "A" * 10001
]

for output in test_outputs:

    try:
        result = validate_output(output)
        print("VALID:", result)

    except ValueError as error:
        print("INVALID:", error)