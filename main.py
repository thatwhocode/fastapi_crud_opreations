from fastapi import FastAPI
from fastapi.exceptions import  HTTPException
from fastapi.responses import Response
from models.models import Fish
app = FastAPI()
fishes =[{"name": "Carasius", "UID": 1, "description":"Add some description text here", "Location":"Krakow"},
        {"name": "Bream", "UID": 2, "description":"Add some description text here", "Location":"Wroclaw"},
         {"name": "Roach", "UID": 3, "description":"Add some description text here", "Location":"Warsawa"} ] 

@app.get("/")
async def hellWorld():
    return{"Hello": "World"}
@app.get("/fishes")
async def list_fishes():
    return fishes
@app.get("/fish/{id}")
async def return_numbered_fish(id : int):
    for record in fishes:
        if record.get("UID") == id:
            return {"fish": record}
    raise HTTPException(status_code=404)


@app.post("/add_fish/")
async def fish_adder( Fish : Fish | None):
    for record in fishes:
        if Fish.id == record.get("UID"):
            raise HTTPException(status_code=403)
    
    if(fishes.insert(Fish.id, Fish.name)):
        return Response(status_code=200)


@app.put("/rewrite_fish_details/")
async  def rewrite_fish_details(Fish : Fish | None):
    for record in fishes:
        if Fish.id == record["UID"]:
            record.update(Fish)
            return Response(status_code=200)

@app.delete("/delete/{id}")
async def delete_fish(id : int):
    for num, record in enumerate(fishes):
        if id == record["UID"]:
            fishes.remove(record)
            return
    return HTTPException(404)    

@app.delete("/delete/all/")
async def delete_all():
    for _, record   in enumerate(fishes):
        fishes.remove(record)
    return