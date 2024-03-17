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
    
@app.get("/users")
async def get_user(db: db_dependency):
    user = db.query(model.User).all()
    return user

@app.get("/user/{user_id}")
async def read_user(user_id: int, db: db_dependency):
    user = db.query(model.User).filter(model.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
    
    return user
    
@app.put("/user/{user_id}")
async def update_user(user_id: int, user: UserBase ,db: db_dependency):
    user_db = db.query(model.User).filter(model.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
    print(user)
     # Update user data
    # for key, value in user.dict(exclude_unset=True).items():
    #     setattr(user, key, value)

    db.commit()
    # db.refresh(user)
    # db.add()
    return user

@app.delete("/user/{user_id}")
async def delete_user(user_id: int , db: db_dependency):
    user = db.query(model.User).filter(model.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
    
    db.delete(user)
    db.commit()
    return "user deleted"