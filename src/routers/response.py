from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from schemas.responses import ResponseSchema, ResponseInSchema
from dependencies import get_db, get_current_user
from sqlalchemy.ext.asyncio import AsyncSession
from queries import response as response_queries
from models import User

router = APIRouter(prefix="/responses", tags=["responses"])


@router.post("", response_model=ResponseSchema)
async def create_response(
        response: ResponseInSchema,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    response = await response_queries.create_response(db=db, response_schema=response, current_user=current_user)

    return ResponseSchema.from_orm(response)


@router.get("/my-responses", response_model=Optional[List[ResponseSchema]])
async def get_my_responses(
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    if id:
        return await response_queries.get_my_responses(db=db, current_user=current_user)

    # return await response_queries.get_my_responses(db=db, current_user=current_user)


@router.get("", response_model=Optional[List[ResponseSchema]])
async def get_response_by_job_id(
        db: AsyncSession = Depends(get_db),
        id: int = 1
):
    return await response_queries.get_responses_by_job_id(db=db, id=id)
