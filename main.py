from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel
from typing import Annotated
from models import model
from config.database import engine, SessionLocal
from sqlalchemy.orm import Session

app = FastAPI(title="Sql Test")
model.Base.metadata.create_all(bind=engine)


class PostBase(BaseModel):
    title: str
    content: str
    user_id: int

class UserBase(BaseModel):
    username: str


def get_db():
    db = SessionLocal()
    try:
         yield db
    finally:
        db.close()
        
db_dependency = Annotated[Session, Depends(get_db)]   


    
@app.get('/')
async def root():
    return "SWL"

@app.post("/users/", status_code=status.HTTP_201_CREATED)
async def create_user_route(user: UserBase, db: db_dependency):
    db_user = model.User(**user.dict())
    db.add(db_user)
    db.commit()