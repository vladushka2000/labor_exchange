from models import User, Response
from schemas.responses import ResponseInSchema
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, status

from dependencies.job import get_current_job


async def create_response(db: AsyncSession, response_schema: ResponseInSchema, current_user: User) -> Response:
    if not current_user.is_company:
        user_id: int = current_user.id
        response = Response(
            user_id=user_id,
            job_id=response_schema.job_id,
            message=response_schema.message
        )

        if get_current_job(response.job_id):
            db.add(response)
            await db.commit()
            await db.refresh(response)

            return response

    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Компания не может делать отклики на вакансии")


async def get_my_responses(db: AsyncSession, current_user: User) -> Optional[List[Response]]:
    if current_user.is_company:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Компания не может делать отклики на вакансии")

    query = select(Response).where(Response.user_id == current_user.id)
    res = await db.execute(query)

    return res.scalars().all()


async def get_responses_by_job_id(db: AsyncSession, id: int) -> Optional[List[Response]]:
    query = select(Response).where(Response.job_id == id)
    res = await db.execute(query)
    res = res.scalars().all()

    return res
