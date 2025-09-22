from pydantic import BaseModel

class Fish(BaseModel):
    name : str
    description : str
    id: int