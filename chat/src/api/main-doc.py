import asyncio
from typing import Literal
from langchain_core.messages import AIMessage, HumanMessage
from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from langgraph.checkpoint.redis.aio  import AsyncRedisSaver
from graph.graph_redis import build_app
from src.graph.state import PatientChatRequest
import uuid 
from uuid import UUID, uuid4
from dotenv import load_dotenv
import redis
import os
load_dotenv()
db_uri = os.getenv("REDIS_URL")
print(db_uri)

# class PatientChatRequest(BaseModel):
#     messages : str
#     thread_id : UUID ##UUID = Field(default_factory=uuid4)
#     status : Literal["Chatting","Done"] = "Chatting"

app = FastAPI(
    title="Redis Check",
    description="Checking for the doctor site is running",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to your frontend domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

graph_app = None
@app.post("/start_interview")
async def start_interview():
    config = {
        "configurable": {
            "thread_id": uuid4()
        }
    }

    async with AsyncRedisSaver.from_conn_string(db_uri) as checkpointer:
        await checkpointer.asetup()
        global graph_app
        graph_app = build_app(checkpointer)
        result = await graph_app.ainvoke(
            {
                "messages": [HumanMessage(content="(start)")]
            },
            config=config
        )  

    return {
        "assistant_reply": result["messages"][-1].content,
        "thread_id" : config["configurable"]['thread_id']
    }

@app.post("/next_message")
async def next_message(req:PatientChatRequest):
    config = {
        "configurable": {
            "thread_id": req.thread_id
        }
    }
    print(graph_app)
    result = await graph_app.ainvoke(
        {"messages":[req.messages]},
        config=config
    )

    return{
        "assistant_reply" : result['messages'][-1].content,
        "thread_id" : req.thread_id
    }






    
