# import sys, os
# sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from auth.controller import router as auth_router
from users.controller import router as user_router
from patients.controller import router as patient_router
from doctors.controller import router as doctor_router
from database.core import Base, engine
from facilites.controller import router as facilites_router 
from scheduling.controller import router as scheduling_router
from doctorFinder.controller import router as doctorFinder_router
from booking.controller import router as booking_router
from chat.controller import router as chat_router
from report.controller import router as report_router
from consultation_session.controller import router as consultation_session_router
from consultation_notes.controller import router as consultation_notes_router

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


Base.metadata.create_all(bind=engine)

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "*"   # allow all for development
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth_router)
app.include_router(user_router)
app.include_router(patient_router)
app.include_router(doctor_router)
app.include_router(facilites_router)
app.include_router(scheduling_router)
app.include_router(doctorFinder_router)
app.include_router(booking_router)
app.include_router(chat_router)
app.include_router(report_router)
app.include_router(consultation_session_router)
app.include_router(consultation_notes_router)
# @app.post("/finish_interview")
# async def finish_interview(session_id: str, doctor_id: UUID, current_user: CurrentUser):

#     # Push report generation task to Redis Queue
#     report_queue.enqueue(
#         generate_reports_job,
#         session_id=session_id,
#         patient_id=current_user.get_uuid(),
#         doctor_id=doctor_id,
#         job_timeout=900  # optional
#     )

    # return {"message": "Report generation started"}


# redis_conn = Redis(host="localhost",port=6380,db=0, decode_responses=False)

# @app.post("/get_chat")
# def get_chat():
#     redis_conn.getrange(,0,-1)

# @app.on_event("startup")    
# async def startup():
#     await init_graph()
#     # Base.metadata.create_all(bind=engine)
@app.get("/")
def hello():
    return {"Hello": "World"}

