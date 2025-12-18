from pydantic import BaseModel
from uuid import UUID

class FacilitiesDetails(BaseModel):
    facilityName : str
    facilityType : str
    facilityAddress : str
    city : str
    state : str
    postalCode : int

class FacilityResponse(FacilitiesDetails):
    id: UUID
    doctor_id : UUID
    
    class Config:
        from_attributes = True

