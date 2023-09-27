from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from ..database import get_async_session
from .models import operation

router = APIRouter(
    prefix="/operations",
    tags=["Operation"]
)

@router.get("/")
async def get_specific_operations(
        operation_type: str,
        session: AsyncSession = Depends(get_async_session)
        ):
    query = select(operation).where(operation.c.type == operation_type)
    result = await session.execute(query)
    return result.all()