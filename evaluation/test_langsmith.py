from langsmith import traceable


@traceable(name="True Claim LangSmith Test")
def test_function():
    return "LangSmith tracing is working!"


if __name__ == "__main__":
    result = test_function()
    print(result)