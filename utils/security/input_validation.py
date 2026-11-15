def validate_claim(claim: str):

    print("\n========== INPUT VALIDATION ==========")

    # Check input type
    if not isinstance(claim, str):
        raise ValueError("Claim must be a string.")

    # Remove unnecessary whitespace
    claim = claim.strip()

    # Check empty input
    if not claim:
        raise ValueError("Claim cannot be empty.")

    # Check maximum length
    MAX_LENGTH = 2000

    if len(claim) > MAX_LENGTH:
        raise ValueError(
            f"Claim is too long. Maximum allowed length is {MAX_LENGTH} characters."
        )

    print("Input validation successful.")

    return claim
