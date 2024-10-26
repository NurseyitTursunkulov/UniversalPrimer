from pydantic import BaseModel
from fastapi import FastAPI
from database import engine, Base, database
import models
import httpx

app = FastAPI()
Base.metadata.create_all(bind=engine)


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


# @app.get("/items/{item_id}")
# async def read_item(item_id: int):
#     return {"item_id": item_id}


@app.get("/external-data/")
async def fetch_external_data():
    url = "https://jsonplaceholder.typicode.com/posts/1"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        data = response.json()
        return {"data": data}


class ItemCreate(BaseModel):
    name: str
    description: str = None
    price: float


class Item(BaseModel):
    name: str
    price: float
    desc: str = None
    tax: float = 0.0


@app.post("/items/")
async def create_item(item: Item):
    query = models.Item.__table__.insert().values(
        name=item.name, description=item.desc, price=item.price, tax=item.tax
    )
    item_id = await database.execute(query)
    return {"item": item_id, "message": "item created succesfuly"}


@app.get("/items/{item_id}")
async def read_item(item_id: int):
    query = models.Item.__table__.select().where(models.Item.id == item_id)
    item = await database.fetch_one(query)
    return {"item": item} if item else {"error": "item not found"}


class ItemUpdate(BaseModel):
    name:str = None
    description :str = None
    price : float = None
    tax:float = None

@app.put("/items/{item_id}")
async def update_item(item_id:int,item:ItemUpdate):
    query = models.Item.__table__.update().where(models.Item.id==item_id).values(
        name=item.name,description = item.description, price=item.price, tax = item.tax
    )
    itemres = await database.execute(query)
    return {"message":"Item updated succesfuly" + str(itemres)}

@app.delete("/items/{item_id}")
async def deleteItem(item_id:int):
    query = models.Item.__table__.delete().where(models.Item.id == item_id)
    await database.execute(query)
    return {"message":"item deleted successfuly"}