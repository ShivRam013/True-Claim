from utils.llm_gateway import llm_completion


messages = [
    {
        "role": "user",
        "content": "Explain how a student placement prediction system works in 5 simple points."
    }
]


response = llm_completion(messages, stream=True)

print("\n========== LITELLM STREAMING TEST ==========\n")

for chunk in response:

    content = chunk.choices[0].delta.content

    if content:
        print(content, end="", flush=True)

print("\n")