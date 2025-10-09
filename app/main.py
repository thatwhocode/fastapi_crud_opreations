from fastapi import FastAPI, Depends, status
from fastapi.exceptions import  HTTPException
from fastapi.responses import Response
from database.database import  get_db, init_db_resources
from database.database_models import Fish, Location
from sqlalchemy.orm import  selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from models.models import  FishResponse, FishBase
from typing import List
from sqlalchemy import select
from contextlib import asynccontextmanager
from sqlalchemy.exc import NoResultFound


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        await init_db_resources()
        yield app
    except Exception as e: 
        print(e)
    finally:
        pass

app = FastAPI(lifespan=lifespan)

@app.get("/")
async def hello_world():
    return{"message": "Hello world"}

@app.get("/fishes/", response_model=List[FishResponse])
async def list_fishes(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    stmt = (select(Fish).options(selectinload(Fish.locations)).offset(skip).limit(limit))
    fishes  = await db.execute(stmt)
    return   fishes.scalars().all()

@app.get("/fishes/{fish_id}", response_model=FishResponse)
async def return_numbered_fish(fish_id : int, db: AsyncSession = Depends(get_db)):
    stmt = (select(Fish).options(selectinload(Fish.locations))).where(Fish.id == fish_id)
    try: 
        numbered_fish = (await db.execute(stmt)).scalar_one()
        return numbered_fish
    except NoResultFound:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, 
                            detail= f"There`s no such fish: {fish_id}")

@app.post("/add_fish/", response_model= FishResponse)
async def add_fishes(fish_data: FishBase,  db: AsyncSession = Depends(get_db)):
    stmt = (select(Fish).options(selectinload(Fish.locations).selectinload(
        Fish.locations))).where(Fish.name == fish_data.name
            )
    
    result = await db.execute(stmt)
    if result:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Fish with this parametrs already exist"
        )
    fish_dict =  fish_data.dict(exclude={'locations'})
    new_fish = Fish(**fish_dict)

    for loc_data in fish_data.locations:
        exsisting_location = await db.scalar(select(Location).where(Location.name == loc_data.name))
        if exsisting_location:
            new_fish.locations.append(exsisting_location)
        else:
            new_location = Location(**loc_data.dict())
            new_fish.locations.append(new_location)
    db.add(new_fish)

    await db.commit()
    await db.refresh(new_fish)


    return new_fish

@app.put("/chagge_fish{fish_id}", 
         response_model=FishResponse)
async def change_fish_data(fish_id: int,
                     fish_update_data : FishBase,
                     db:AsyncSession = Depends(get_db)):
    stmt  = (select((Fish)).options(selectinload(Fish.locations))).where(Fish.id == fish_id)
    result = await db.execute(stmt)
    existing_fish = result.scalar_one_or_none()
    if not existing_fish:
        raise HTTPException(
            status_code=404,
            detail="There`s no such fish, thus you can not modify it"
        )

    existing_fish.name = fish_update_data.name
    existing_fish.description = fish_update_data.description
    existing_fish.locations.clear()
    for loc_data in fish_update_data.locations:
        querystmt = select(Location).where(Location.name == loc_data.name)
        existing_loc = await db.scalar(querystmt)
        if existing_loc:
            existing_fish.locations.append(existing_loc)
        else:
            new_loc = Location(**loc_data.dict())
            db.add(new_loc)
            existing_fish.locations.append(new_loc)

    await db.commit()

    await db.refresh(existing_fish)
    return existing_fish
@app.delete("/delete/{fish_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_numbrered_fish(fish_id : int, db: AsyncSession = Depends(get_db)):
    try:
        stmt = select(Fish).where(Fish.id == fish_id).options(selectinload(Fish.locations))
        result = await db.execute(stmt)
        existing_fish = result.scalar_one()
        await db.delete(existing_fish)
        await db.commit()
    except NoResultFound:
        raise HTTPException(status_code=404, detail="No such fish found")
    return(Response(status_code=status.HTTP_204_NO_CONTENT))