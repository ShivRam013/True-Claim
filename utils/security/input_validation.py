MAX_LENGTH = 2000


def validate_claim(claim: str):
    """Validate the user's claim before processing."""

    print("\n========== INPUT VALIDATION ==========")

    # Check input type
    if not isinstance(claim, str):
        raise ValueError("Claim must be a string.")

    # Remove unnecessary whitespace
    claim = claim.strip()

    # Check for empty input
    if not claim:
        raise ValueError("Claim cannot be empty.")

    # Enforce the maximum claim length
    if len(claim) > MAX_LENGTH:
        raise ValueError(
            f"Claim is too long. Maximum allowed length is "
            f"{MAX_LENGTH} characters."
        )

    print("Input validation successful.")

    return claim