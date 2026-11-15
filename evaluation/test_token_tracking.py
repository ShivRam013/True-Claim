from dotenv import load_dotenv
load_dotenv()

from utils.llm_gateway import llm_completion

response = llm_completion(
    messages=[
        {"role": "user", "content": "Reply with: True Claim is working."}
    ],
    temperature=0
)

print("LLM Response:", response)