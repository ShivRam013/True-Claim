from retrieval.hybrid_search import hybrid_search


claim = """
LoRA reduces the number of trainable parameters compared with full fine-tuning.
"""

results = hybrid_search(claim)

for i, result in enumerate(results, start=1):

    print("\n-----------------------")
    print(f"Result {i}")
    print(f"Score: {result['score']}")
    print(f"Text: {result['text'][:300]}")
    print(f"Metadata: {result['metadata']}")