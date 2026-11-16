import os

from dotenv import load_dotenv


# Load environment variables from .env
load_dotenv()

# Groq API configuration
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

GROQ_MODEL = os.getenv(
    "GROQ_MODEL",
    "openai/gpt-oss-120b",
)

# Ensure the API key is configured
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY is missing in .env")