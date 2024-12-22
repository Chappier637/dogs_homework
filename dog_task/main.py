
from enum import Enum
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


class Breed(str, Enum):
    setter = "setter"
    bulldog = "bulldog"
    york = "york"


class Dog(BaseModel):
    name: str
    id: int
    breed: Breed


class Timestamp(BaseModel):
    id: int
    timestamp: int


db = {
    0: Dog(name='Dog1', id=0, breed='setter'),
    1: Dog(name='Dog2', id=1, breed="bulldog"),
    2: Dog(name='Dog3', id=2, breed='york'),
    3: Dog(name='Dog4', id=3, breed='york'),
    4: Dog(name='Dog5', id=4, breed='york'),
    5: Dog(name='Dog6', id=5, breed='bulldog'),
    6: Dog(name='D0g6', id=6, breed='bulldog')
}

post_db = [
    Timestamp(id=0, timestamp=12),
    Timestamp(id=1, timestamp=10)
]


@app.get("/")
def root():
    return "This is server's root."

@app.post("/post")
def get_post():
    return {"id": 0, "timestamp": 0}

@app.get("/dog")
def get_dogs(breed: Breed):
    return [dog for dog in db.values() if dog.breed == breed]

@app.post("/dog")
def create_dog(dog: Dog):
    if db.get(dog.id) != None:
        raise HTTPException(status_code=422, detail="id already exists")
    
    db[dog.id] = dog
    return dog

@app.get("/dog/{id}")
def get_dog_by_id(id: int):
    return db.get(id)

@app.patch("/dog/{id}")
def update_dog(id: int, dog: Dog):
    if db.get(dog.id) == None:
        raise HTTPException(status_code=422, detail="id doesn't exists")
    
    if  id != dog.id:
        raise HTTPException(status_code=422, detail="id doesn't match request's body")
    
    db[id] = dog
    return dog