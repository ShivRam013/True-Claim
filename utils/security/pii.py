import re


# Patterns for detecting common personally identifiable information
PII_PATTERNS = {
    "EMAIL": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",
    "PHONE": r"(?<!\w)(?:\+91[\s-]?)?[6-9]\d{9}(?!\w)",
    "AADHAAR": r"(?<!\d)\d{4}[\s-]?\d{4}[\s-]?\d{4}(?!\d)",
    "PAN": r"\b[A-Z]{5}[0-9]{4}[A-Z]\b",
    "CREDIT_CARD": r"(?<!\d)(?:\d[ -]?){13,19}(?!\d)",
}


def anonymize_pii(text: str):
    """Detect and replace common PII patterns with placeholders."""

    for entity_type, pattern in PII_PATTERNS.items():
        text = re.sub(
            pattern,
            f"[{entity_type}]",
            text,
            flags=re.IGNORECASE,
        )

    return text