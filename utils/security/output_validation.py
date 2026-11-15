def validate_output(response: str):

    print("\n========== OUTPUT VALIDATION ==========")

    # Check output type
    if not isinstance(response, str):
        raise ValueError("LLM output must be a string.")

    # Remove unnecessary whitespace
    response = response.strip()

    # Check empty output
    if not response:
        raise ValueError("LLM returned an empty response.")

    # Check maximum output length
    MAX_LENGTH = 10000

    if len(response) > MAX_LENGTH:
        raise ValueError(
            f"LLM output exceeds the maximum length of {MAX_LENGTH} characters."
        )

    print("Output validation successful.")

    return response