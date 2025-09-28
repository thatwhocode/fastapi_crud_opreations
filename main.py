from fastapi import FastAPI, Depends, status
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
@app.get("/fishes/{fish_id}", response_model=FishResponse)
def return_numbered_fish(fish_id : int, db: Session = Depends(get_db)):
    numbered_fish = db.query(Fish).filter(Fish.id == fish_id).first()
    if numbered_fish: 
        return numbered_fish
    else:
        raise HTTPException(
            status_code=404,
            detail="Fish with this number does not exists"
        )
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
@app.put("/chagge_fish{fish_id}", 
         response_model=FishResponse)
def change_fish_data(fish_id: int,
                     fish_update_data : FishBase,
                     db:Session = Depends(get_db)):
    
    existing_fish = db.query(Fish).filter(Fish.id == fish_id).first()
    if not existing_fish:
        raise HTTPException(
            status_code=404,
            detail="There`s no such fish, thus you can not modify it"
        )
    location_list = []
    for loc_data in fish_update_data.locations:
        exsisting_loc = db.query(Location).filter(Location.name == loc_data.name).first()
        if exsisting_loc:
            location_list.append(exsisting_loc)
        else:
            new_loc = Location(name = loc_data.name, region = loc_data.region)
            db.add(new_loc)
            location_list.append(new_loc)
    existing_fish.name = fish_update_data.name
    existing_fish.description = fish_update_data.description
    existing_fish.locations = location_list
    db.commit()
    db.refresh(existing_fish)

    return existing_fish
@app.delete("/delete/{fish_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_numbrered_fish(fish_id : int, db: Session = Depends(get_db)):
    existing_fish = db.query(Fish).filter(Fish.id == fish_id).first()
    if not existing_fish:
        raise HTTPException(
            status_code= 404,
            detail="No such fish found"
        )
    db.delete(existing_fish)
    db.commit()
    return(Response(status_code=status.HTTP_204_NO_CONTENT))