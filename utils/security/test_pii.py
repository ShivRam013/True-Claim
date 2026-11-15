from utils.security.middleware import pii_middleware

claim = """
My email is rahul@example.com.
My phone is +91 9876543210.
Can LoRA reduce fine-tuning costs?
"""

result = pii_middleware(claim)

print("\nSanitized Claim:")
print(result)