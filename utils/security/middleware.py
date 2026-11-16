from utils.security.pii import anonymize_pii


def pii_middleware(claim: str):
    """Anonymize personally identifiable information in the claim."""

    print("\n========== PII MIDDLEWARE ==========")

    sanitized_claim = anonymize_pii(claim)

    if sanitized_claim != claim:
        print("PII detected and anonymized.")
    else:
        print("No PII detected.")

    return sanitized_claim