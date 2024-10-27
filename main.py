from pydantic import BaseModel
from fastapi import FastAPI, Depends, HTTPException, status

from auth import create_access_token
from database import engine, Base, database
from fastapi.security import OAuth2PasswordRequestForm
import models
import userDb
import httpx
import auth

app = FastAPI()
Base.metadata.create_all(bind=engine)


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = userDb.authenticate_user(userDb.fake_users_db, form_data.username, form_data.password)
    print()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )
    access_token = create_access_token(data={"sub": user["username"]})
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/user/me")
async def read_users_me(token: str = Depends(userDb.oauth2_scheme)):
    user = auth.verify_token(token)
    if user is None:
        raise HTTPException(status_code=401, detail="invalid token")
    return {"username": user["sub"]}


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
    name: str = None
    description: str = None
    price: float = None
    tax: float = None


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: ItemUpdate):
    query = models.Item.__table__.update().where(models.Item.id == item_id).values(
        name=item.name, description=item.description, price=item.price, tax=item.tax
    )
    itemres = await database.execute(query)
    return {"message": "Item updated succesfuly" + str(itemres)}


@app.delete("/items/{item_id}")
async def deleteItem(item_id: int):
    query = models.Item.__table__.delete().where(models.Item.id == item_id)
    await database.execute(query)
    return {"message": "item deleted successfuly"}
