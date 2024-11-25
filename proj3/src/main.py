import models

from pydantic import BaseModel
from fastapi import FastAPI, Depends, HTTPException, Path
from typing import Annotated
from sqlalchemy.orm import Session
from models import Todos, TodoRequest
from database import engine, SessionLocal
from starlette import status
from router import auth, todos, admin, user

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(user.router)
