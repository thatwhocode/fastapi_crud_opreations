from pydantic import BaseModel
from typing import List

class LocationBase(BaseModel):
    name: str
    region: str


class FishBase(BaseModel):
    name : str
    description : str
    locations: List[LocationBase]

class FishCreate(FishBase):
    pass

class FishResponse(FishBase):
    id: int
    class Config: 
        from_attributes = True