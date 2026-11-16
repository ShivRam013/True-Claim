import time

from langsmith import get_current_run_tree, traceable
from litellm import RateLimitError, completion

from utils.config import GROQ_API_KEY, GROQ_MODEL


MAX_RETRIES = 3


@traceable(name="LLM Completion", run_type="llm")
def llm_completion(
    messages,
    temperature=0,
    stream=False,
    model=None,
    api_key=None,
):
    """Call an LLM through LiteLLM with retries and LangSmith tracking."""

    selected_model = model or f"groq/{GROQ_MODEL}"
    selected_api_key = api_key or GROQ_API_KEY

    for attempt in range(MAX_RETRIES):
        try:
            response = completion(
                model=selected_model,
                messages=messages,
                api_key=selected_api_key,
                temperature=temperature,
                timeout=30,
                stream=stream,
            )

            # Return the stream directly without processing token usage
            if stream:
                return response

            # Capture token usage in LangSmith
            run = get_current_run_tree()

            if run and response.usage:
                usage = response.usage

                input_tokens = usage.prompt_tokens or 0
                output_tokens = usage.completion_tokens or 0
                total_tokens = usage.total_tokens or (
                    input_tokens + output_tokens
                )

                run.set(
                    usage_metadata={
                        "input_tokens": input_tokens,
                        "output_tokens": output_tokens,
                        "total_tokens": total_tokens,
                    }
                )

                run.metadata.update({
                    "ls_provider": "groq",
                    "ls_model_name": selected_model,
                })

            return response.choices[0].message.content

        except RateLimitError:
            # Retry when the API rate limit is reached
            if attempt == MAX_RETRIES - 1:
                raise

            wait_time = 10 * (attempt + 1)

            print(
                f"Groq rate limit reached. "
                f"Retrying in {wait_time} seconds..."
            )

            time.sleep(wait_time)