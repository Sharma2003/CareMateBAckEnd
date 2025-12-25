from pydantic import BaseModel
from uuid import UUID
from datetime import time

class FacilityItem(BaseModel):
    id : UUID
    facilityName : str
    facilityType : str
    city : str

class DoctorItem(BaseModel):
    id : UUID
    first_name: str
    last_name: str

# class SlotItem(BaseModel):
#     start_time = time
#     end_time = time