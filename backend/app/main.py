from fastapi import FastAPI, Depends
from pydantic import BaseModel, Field
from enum import Enum
from fastapi_users import FastAPIUsers

from typing import Optional, Annotated
from datetime import datetime

from .auth.base_config import auth_backend, fastapi_users
from .auth.schemas import UserRead, UserCreate
from .auth.models import User
from .auth.manager import get_user_manager

from .operations.router import router as router_opration

app = FastAPI(
    title="Trading app"
)

@app.get("/")
async def root():
    return {"message": "Hello World"}

app.include_router(
    fastapi_users.get_auth_router(auth_backend, requires_verification=True),
    prefix="/auth/jwt",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

app.include_router(
    router_opration
)