# autograder/autograder_service.py
from token_manager import TokenManager

# If you use OpenAI via LangChain:
try:
    from langchain.callbacks import get_openai_callback
except Exception:
    get_openai_callback = None

def grade_with_logging(user_id: str, chain, payload: dict, model_name="gpt-4o"):
    """
    Wrap your autograder chain call here.
    Example:
        result = chain.invoke({"student_answer": "...", "rubric": "..."})
    """
    if get_openai_callback is None:
        # Fallback if callbacks unavailable: run, then you must compute/log tokens yourself
        result = chain.invoke(payload)
        # TokenManager.log_usage(user_id, tokens=<estimate>, cost=<calc>, model=model_name, task="autograde")
        return result

    with get_openai_callback() as cb:
        result = chain.invoke(payload)
        TokenManager.log_usage(
            user_id=user_id,
            tokens=cb.total_tokens,
            cost=cb.total_cost,
            model=model_name,
            task="autograde",
        )
    return result

# For non-OpenAI models (Gemini, etc.), call your chain and then:
# TokenManager.log_usage(user_id, tokens=<your_count>, cost=<usd>, model="gemini-1.5", task="autograde")
