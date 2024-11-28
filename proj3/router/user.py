from fastapi import APIRouter, Depends, HTTPException, Path
from typing import Annotated
from sqlalchemy.orm import Session
from starlette import status
from pydantic import BaseModel, Field
from .auth import get_current_user, SECRET_KEY, ALGORITHM, bcrypt_context
from ..models import Todos, TodoRequest, Users
from ..database import SessionLocal


router = APIRouter(
    prefix='/user',
    tags=['user']
)



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
    
    
db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

class UserVerification(BaseModel):
    old_password: str
    new_password: str = Field(min_length=6)


def authentice_user(usersname: str, password: str, db):
    user = db.query(Users).filter(Users.username == usersname).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return user


@router.get("/", status_code=status.HTTP_200_OK)
async def get_user(user: user_dependency, db: db_dependency):
    if user is None or user.get('role') == 'admin':
        raise HTTPException(status_code=401, detail='Authentication Failed')
    
    return db.query(Users).filter(Users.id == user.get('id')).first()


@router.put("/change_password", status_code=status.HTTP_204_NO_CONTENT)
async def change_password(user: user_dependency, 
                          db: db_dependency,
                          user_verification: UserVerification):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    user_model = db.query(Users).filter(Users.id == user.get('id')).first()
    
    if not bcrypt_context.verify(user_verification.old_password, user_model.hashed_password):
        raise HTTPException(status_code=401, detail='Error on password change.')
    user_model.hashed_password = bcrypt_context.hash(user_verification.new_password)
    db.add(user_model)
    db.commit()
    
    
    
@router.put("/change_phone_number", status_code=status.HTTP_204_NO_CONTENT)
async def change_phone_number(user: user_dependency, 
                          db: db_dependency,
                          user_verification: UserVerification,
                          new_phone_number: str):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    user_model = db.query(Users).filter(Users.id == user.get('id')).first()
    user_model.phone_number = new_phone_number
    db.add(user_model)
    db.commit()
    
    