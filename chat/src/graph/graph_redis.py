from langgraph.graph import StateGraph, END, START
from langgraph.checkpoint.redis import RedisSaver
from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage

from chat.src.graph.state import InterviewState, add_messages
from chat.src.graph.nodes import ask_question, update_report, summarize_chat
from chat.src.graph.edges import finalize_node, should_continue 

class BaseChatState(TypedDict):
    messages : Annotated[list[BaseMessage],add_messages]
    question_count : int


def build_app(checkpointer):
    g = StateGraph(BaseChatState)

    g.add_node("ask_question", ask_question)
    g.add_node("update_report", update_report)
    g.add_node("finalize", finalize_node)
    g.add_node("summarize_chat", summarize_chat)

    g.add_edge(START, "ask_question")
    # g.add_edge("ask_question", "update_report")
    g.add_conditional_edges(
        "ask_question",
        should_continue,
        {"wait_for_user": END, "finalize": "finalize"}
    )
    g.add_edge("finalize", "update_report")
    g.add_edge("ask_question", END)
    return g.compile(checkpointer=checkpointer)

