from datetime import datetime

from fastapi import Depends
from fastapi_users.db import SQLAlchemyBaseUserTable, SQLAlchemyUserDatabase
from sqlalchemy import (JSON, TIMESTAMP, Boolean, Column, ForeignKey, Integer,
                        MetaData, String, Table)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column

from ..database import get_async_session, Base

metadata = MetaData()

role = Table(
    "role",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String, nullable=False),
    Column("permissions", JSON),
)

user = Table(
    "user",
    metadata,
    Column(
        "id", Integer, 
        primary_key=True
    ),
    Column(
        "username", String, 
        nullable=False
    ),
    Column(
        "registered", TIMESTAMP, 
        default=datetime.utcnow
    ),
    Column(
        "role_id", Integer, 
        ForeignKey("role.id")
    ),
    Column(
        "email", String(length=320), 
        unique=True, index=True, nullable=False
    ),
    Column(
        "hashed_password", String(length=1024), 
        nullable=False
    ),
    Column(
        "is_active", Boolean, 
        default=True, nullable=False
    ),
    Column(
        "is_superuser", Boolean, 
        default=False, nullable=False
    ),
    Column(
        "is_verified", Boolean, 
        default=False, nullable=False
    ),
)


class User(SQLAlchemyBaseUserTable[int], Base):
    id = Column("id", Integer, primary_key=True)
    username = Column("username", String, nullable=False)
    registered = Column("registered", TIMESTAMP, default=datetime.utcnow)
    role_id = Column("role_id", Integer, ForeignKey(role.c.id))
    email: Mapped[str] = mapped_column(
        String(length=320), unique=True, index=True, nullable=False
    )
    hashed_password: Mapped[str] = mapped_column(
        String(length=1024), nullable=False
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )
    is_verified: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )



async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)