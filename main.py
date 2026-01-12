from fastapi import FastAPI
from chat.src.utils.runtime import init_graph

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
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(patient_router)
app.include_router(doctor_router)
app.include_router(facilites_router)
app.include_router(scheduling_router)
app.include_router(doctorFinder_router)
app.include_router(booking_router)
app.include_router(chat_router)

# @app.on_event("startup")    
# async def startup():
#     await init_graph()
#     # Base.metadata.create_all(bind=engine)
@app.get("/")
def hello():
    return {"Hello": "World"}

