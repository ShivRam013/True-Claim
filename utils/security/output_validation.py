MAX_LENGTH = 10000


def validate_output(response: str):
    """Validate the final LLM response before returning it."""

    print("\n========== OUTPUT VALIDATION ==========")

    # Check output type
    if not isinstance(response, str):
        raise ValueError("LLM output must be a string.")

    # Remove unnecessary whitespace
    response = response.strip()

    # Check for empty output
    if not response:
        raise ValueError("LLM returned an empty response.")

    # Enforce the maximum output length
    if len(response) > MAX_LENGTH:
        raise ValueError(
            f"LLM output exceeds the maximum length of "
            f"{MAX_LENGTH} characters."
        )

    print("Output validation successful.")

    return response