from utils.llm_gateway import llm_completion


messages = [
    {
        "role": "user",
        "content": "What is machine learning? Explain in one sentence."
    }
]


response = llm_completion(
    messages,
    model="groq/openai/gpt-oss-120b"
)

print("\n========== MODEL SWITCHING TEST ==========")
print(response)