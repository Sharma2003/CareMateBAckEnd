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
    
    class Config:
        orm_mode = True

