from retrieval.claim_decomposition import decompose_claim


claim = """
student placement prediction project predict the student placed or not placed using students 100000 data"""

result = decompose_claim(claim)

print("\n========== CLAIM DECOMPOSITION ==========\n")
print(result)