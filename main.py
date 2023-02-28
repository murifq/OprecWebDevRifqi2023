from fastapi import FastAPI,status,HTTPException
from pydantic import BaseModel, Field
from typing import Optional,List, Dict
from database import SessionLocal
import models
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timezone
from uuid import uuid4, UUID


app = FastAPI()

origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



class Item(BaseModel):
    id_post: UUID = Field(default_factory=uuid4)
    caption: str
    post_date: datetime = Field(default_factory=datetime.utcnow)


    class Config:
        orm_mode=True

db=SessionLocal()
@app.get("/posts", response_model=List[Item], status_code=200)
def get_all_item():
    items=db.query(models.Item).all()
    return items


@app.get("/posts/{id_post}", response_model=Item, status_code=status.HTTP_200_OK)
def get_an_item(id_post:int):
    item=db.query(models.Item).filter(models.Item.id_post==id_post).first()
    return item


@app.post("/posts", response_model=Item, status_code=status.HTTP_201_CREATED)
def create_an_item(item:Item):
    # db_item=db.query(models.Item).filter(models.Item.id_post==item.id_post).first()

    # if db_item is not None:
    #     raise HTTPException(status_code=400, detail="Item already exists")
    new_item=models.Item(
        id_post=uuid4(),
        caption=item.caption,
        post_date = datetime.now(timezone.utc)
    )
    db.add(new_item)
    db.commit()
    return new_item

    

@app.put("/edit/{id_post}",response_model=Item, status_code=status.HTTP_200_OK)
def update_an_item(item:Item, id_post:str):
    item_to_update=db.query(models.Item).filter(models.Item.id_post==id_post).first()
    item_to_update.id_post=uuid4()
    item_to_update.caption=item.caption
    item_to_update.post_date=datetime.now(timezone.utc)
    db.commit()
    return item_to_update


@app.delete("/delete/{id_post}")
def delete_item(id_post:str):
    item_to_delete=db.query(models.Item).filter(models.Item.id_post==id_post).first()
    if item_to_delete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,details="Resource Not Found")
    db.delete(item_to_delete)
    db.commit()
    return item_to_delete