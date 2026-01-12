import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import asyncio
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langchain_core.messages import HumanMessage

from graph.graph import build_app
from graph.state import InterviewState
from src.core.prompts import DOCTOR_DEFAULT_REPORT_TEMPLATE, PATIENT_DEFAULT_REPORT_TEMPLATE

# ----------------------------------------------------------------------
# Initialize FastAPI
# ----------------------------------------------------------------------
app = FastAPI(
    title="Doctor Appointment AI Agent",
    description="Conversational AI for patient interviews & medical report generation.",
    version="1.0.0",
)

# Enable CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to your frontend domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

agent = build_app()
sessions = {}


class PatientMessage(BaseModel):
    session_id : str
    patient_reply : str



@app.post("/start_interview/")
async def start_interview():
    session_id = str(asyncio.get_event_loop().time())
    print(f"New session started: {session_id}")

    state = {
        "messages" : [HumanMessage(content="(start)")],
        "summary" : [],
        "question_count" : 0,
        "doctor_report_md" : DOCTOR_DEFAULT_REPORT_TEMPLATE,
        "patient_report_md" : PATIENT_DEFAULT_REPORT_TEMPLATE,
        "done" : False
    }

    updated_state = await agent.ainvoke(state, config={"configurable" : {"thread_id" : session_id}})
    sessions[session_id] = updated_state
    ai_message = updated_state["messages"][-1].content


    return {

        "session_id" : session_id,
        "assistant_reply" : ai_message,
        "done" : updated_state["done"]

    }

@app.post("/next_message/")
async def next_message(data : PatientMessage):

    session_id = data.session_id
    patient_reply = data.patient_reply

    if session_id not in sessions:
        raise HTTPException(status_code=404,detail="Session id not found. start a new interview")
    
    state = sessions[session_id]
    state["messages"].append(HumanMessage(content=patient_reply))
    
    update_state = await agent.ainvoke(state, config={"configurable":{"thread_id":session_id}})
    sessions[session_id] = update_state
    ai_message = update_state["messages"][-1].content

    if update_state["done"]:
        print(f"Interview completed for session {session_id}")
        report = update_state["doctor_report_md"]

        return {
            "assistant_reply":ai_message,
            "final_report" : report,
            "done" : True
        }
        
    return{
        "assistant_reply" : ai_message,
        "done":False
    }


@app.get("/get_report/doctor_report/{session_id}")
async def get_doctor_report(session_id : str):
    if session_id not in sessions:
        raise HTTPException(status_code=404,detail="Session Not Found")
    state = sessions[session_id]
    return {"doctor_report" : state.get("doctor_report_md","Report not yet ready")}


@app.get("/get_report/patient_report/{session_id}")
async def get_patient_report(session_id : str):
    if session_id not in sessions:
        HTTPException(status_code=404, detail="patient_report")
    state = sessions[session_id]
    return {"patient_report" : state.get("patient_report_md","Report not yet ready")}

@app.get("/get_summary/{session_id}")
async def get_summary(session_id : str):
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    state = sessions[session_id]
    return {
        "summary": state.get("summary","Not Ready Yet")
    }


async def root():
    return {"message": "🩺 Doctor Appointment AI Chat Agent is running!"}


# ----------------------------------------------------------------------
# Local run entrypoint
# ----------------------------------------------------------------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api.main:app", host="127.0.0.1", port=8000, reload=True)