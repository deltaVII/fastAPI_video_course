from fastapi import FastAPI
from pydantic import BaseModel, Field
from enum import Enum

from typing import Optional
from datetime import datetime

app = FastAPI(
    title="Trading app"
)

@app.get("/")
async def root():
    return {"message": "Hello World"}

fake_users = [
    {"id": 1, "name": "one", "role": 
        {"id": 1, "date": "2020-01-01T00:00:00", "type_role": "one"} 
    },
    {"id": 2, "name": "onwe"}
]

fake_trades = [
    {"id": 1, "price": 1.0, "quantity": 1.0, "side": "buy"},
    {"id": 2, "price": 1.0, "quantity": 1.0, "side": "sell"},
]

class Trade(BaseModel):
    id: int
    price: float
    quantity: float = Field(ge=0)
    side: str = Field(max_length=5, default="sell")


class RoleType(Enum):
    one = "one"
    two = "two"

class Role(BaseModel):
    id: int
    date: datetime
    type_role: RoleType

class User(BaseModel):
    id: int
    name: str
    role: Optional[Role] = None
    # или Role | None = None

@app.post("/trades")
async def post_trades(trades: list[Trade]):
    fake_trades.extend(trades)
    return fake_trades


@app.get("/users/{user_id}", response_model=list[User])
async def get_user(user_id: int):
    return [user for user in fake_users if user.get("id") == user_id]
