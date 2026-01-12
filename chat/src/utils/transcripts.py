# chat/src/utils/transcript.py
from langchain.messages import SystemMessage, HumanMessage
from langgraph.graph.message import AnyMessage
from typing import List

def build_interview_transcript(messages: List[AnyMessage]) -> str:
    lines = []
    for m in messages:
        if isinstance(m, SystemMessage):
            continue
        role = "PATIENT" if isinstance(m, HumanMessage) else "ASSISTANT"
        lines.append(f"{role}: {m.content}")
    return "\n".join(lines)
