from graph.state import InterviewState
from core.prompts import CLOSING_LINE
from langchain.messages import AIMessage

async def should_continue(state: InterviewState) -> str:
    """Route: keep looping until we've asked 20 questions (or user stops responding)."""
    if state["done"]:
        return "finalize"
    # If the last assistant message was the closing line, also finalize.
    if state["messages"] and isinstance(state["messages"][-1], AIMessage) and CLOSING_LINE in state["messages"][-1].content:
        return "finalize"
    return "wait_for_user"



async def finalize_node(state: InterviewState) -> InterviewState:
    """No-op: terminal cleanup point (you can persist the report here if needed)."""
    return state
