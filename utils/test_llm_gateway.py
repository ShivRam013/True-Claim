from utils.llm_gateway import llm_completion


messages = [
    {
        "role": "system",
        "content": "You are a helpful AI assistant."
    },
    {
        "role": "user",
        "content": "Explain student placement prediction in 2 sentences."
    }
]


response = llm_completion(messages)

print("\n========== LITELLM GATEWAY TEST ==========")
print(response)