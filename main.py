from fastapi import FastAPI, Depends
from fastapi.exceptions import  HTTPException
from fastapi.responses import Response
from database.database import Base, engine, get_db, SessionLocal
from database.database_models import Fish, Location
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from models.models import  FishResponse, FishBase
from typing import List
app = FastAPI()
Base.metadata.create_all(bind = engine)
get_db()
@app.get("/")
async def hello_world():
    return{"message": "Hello world"}

@app.get("/fishes/", response_model=List[FishResponse])
def list_fishes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    fishes  = db.query(Fish).offset(skip).limit(limit).all()
    if fishes is None:
        return[]
    return fishes

@app.post("/add_fish/", response_model= FishResponse)
def add_fishes(fish_data: FishBase,  db: Session = Depends(get_db)):
    existinbg_fish = db.query(Fish).filter(Fish.name == fish_data.name).first()
    if existinbg_fish:
        raise HTTPException(
            status_code=409,
            detail="Fish with this name already exist"
        )
    fish_dict = fish_data.dict(exclude={'locations'})
    new_fish = Fish(**fish_dict)

    for loc_data in fish_data.locations:
        location_obj = db.query(Location).filter(Location.name == loc_data.name).first()
        if not location_obj:
            location_obj = Location(**loc_data.dict())
            db.add(location_obj)
        new_fish.locations.append(location_obj)
    db.add(new_fish)
    db.commit()
    db.refresh(new_fish)
    return new_fish