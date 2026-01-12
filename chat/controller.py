from fastapi import APIRouter, HTTPException
from uuid import UUID, uuid4
from langgraph.checkpoint.redis.aio import AsyncRedisSaver
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv
import os

from helper.ensure import ensure_patient_role
from chat.src.utils.runtime import graph_app
from chat.src.graph.state import InterviewState, PatientChatRequest
from chat.src.graph.graph_redis import build_app
from auth.service import CurrentUser
# from database.core import DbSession
from sqlalchemy.orm import Session

load_dotenv()
db_uri = os.getenv("REDIS_URL")

router = APIRouter(
    prefix="/chat",
    tags=["chat"]
)

graph_app = None
@router.post("/start_interview")
async def start_interview(current_user: CurrentUser):
    # ensure_patient_role(db=Session,current_user=current_id.get_uuid())
    global graph_app
    config = {
        "configurable":{"thread_id":uuid4()}
    }
    async with AsyncRedisSaver.from_conn_string(db_uri) as saver:
        await saver.asetup()

        graph_app = build_app(checkpointer=saver)

    print(graph_app)
    result = await graph_app.ainvoke(
        {"messages": [HumanMessage(content="(start)")]},
        config=config
    )

    return {
        "assistant_reply": result["messages"][-1].content,
        "thread_id": config["configurable"]["thread_id"]
    }

@router.post("/next_message")
async def next_message(req: PatientChatRequest):
    result = await graph_app.ainvoke(
        {"messages": [req.messages]},
        config={"configurable": {"thread_id": req.thread_id}}
    )

    return {
        "assistant_reply": result["messages"][-1].content,
        "thread_id": req.thread_id
    }
