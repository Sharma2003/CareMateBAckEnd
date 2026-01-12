import sys, os


from typing import Annotated, List, TypedDict, Literal
from uuid import UUID
from pydantic import BaseModel
from langgraph.graph.message import add_messages, AnyMessage

class InterviewState(TypedDict):
    messages: Annotated[List[AnyMessage], add_messages]
    summary : list[str]
    question_count: int
    report_md: str
    doctor_report_md:str
    patient_report_md:str
    done: bool

class PatientChatRequest(BaseModel):
    messages : str
    thread_id : UUID ##UUID = Field(default_factory=uuid4)
    status : Literal["Chatting","Done"] = "Chatting"
