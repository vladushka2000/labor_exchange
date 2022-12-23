from typing import List, Optional

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from queries.job import get_job_by_id
from models import User, Response
from schemas.responses import ResponseInSchema


async def create_response(db: AsyncSession,
                          response_schema: ResponseInSchema,
                          current_user: User) -> Response | HTTPException:
    try:
        current_job = await get_job_by_id(db=db, id=response_schema.job_id)
    except HTTPException:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail="Вакансия не найдена")
    else:
        if not current_job.is_active:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="Вакансия не активна")

    if current_user.is_company:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Компания не может делать отклики на вакансии")

    user_id: int = current_user.id
    response = Response(
        user_id=user_id,
        job_id=response_schema.job_id,
        message=response_schema.message
    )

    db.add(response)
    await db.commit()
    await db.refresh(response)

    return response



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
