import asyncio
from uuid import uuid4
from langchain_core.messages import HumanMessage
from langgraph.graph import StateGraph, END, START
from graph.state import InterviewState
from graph.nodes import ask_question, update_report, summarize_chat
from graph.edges import finalize_node, should_continue
from langgraph.checkpoint.memory import MemorySaver
from core.prompts import DOCTOR_DEFAULT_REPORT_TEMPLATE, PATIENT_DEFAULT_REPORT_TEMPLATE    
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
from psycopg_pool import AsyncConnectionPool
from psycopg.rows import dict_row
from IPython.display import Image

def build_app():
    g = StateGraph(InterviewState)

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
    return g.compile(checkpointer=MemorySaver())


# async def run_interview():
#     app = build_app()
#     async def turn(state: InterviewState):
#         return await app.ainvoke(state, config={"configurable": {"thread_id": 1}})

#     # Initialize session
#     state = {
#         "messages": [HumanMessage(content="(start)")],
#         "summary": [],
#         "question_count": 0,
#         # "patient_name": "John Doe",
#         "doctor_report_md": DOCTOR_DEFAULT_REPORT_TEMPLATE,
#         "patient_report_md": PATIENT_DEFAULT_REPORT_TEMPLATE,
#         "done": False,
#     }

#     # summary = {"ASSISTANT": [], "PATIENT": []}

#     try:
#         # Initial response
#         state = await turn(state)
#         summary = {"ASSISTANT": [], "PATIENT": []}
#         print(f"\nASSISTANT: {state['messages'][-1].content}")
#         summary["ASSISTANT"].append(state["messages"][-1].content)

#         for _ in range(25):
#             user_reply = input("\nPATIENT: ").strip()
#             state["messages"].append(HumanMessage(content=user_reply))
#             state = await turn(state)

#             assistant_reply = state["messages"][-1].content
#             summary["PATIENT"].append(user_reply)
#             summary["ASSISTANT"].append(assistant_reply)

#             print(f"\nASSISTANT: {assistant_reply}\n{'-' * 26}")
#             if state["done"]:
#                 break

#     except NotImplementedError as e:
#         print(f"\n[!] Plug in Med-Gemma first: {e}")

#     return {
#         "doctor_report_md": state["doctor_report_md"],
#         "patient_report_md": state["patient_report_md"]
#     }


# if __name__ == "__main__":
#     result = asyncio.run(run_interview())  
#     # print(asyncio.run(run_interview()))
#     print("\n=== DOCTOR REPORT ===")
#     print(result["doctor_report_md"])
#     print("\n=== PATIENT REPORT ===")
#     print(result["patient_report_md"])