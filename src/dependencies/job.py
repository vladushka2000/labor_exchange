from fastapi import Depends, HTTPException, status
from queries import job as job_queries
from sqlalchemy.ext.asyncio import AsyncSession
from dependencies.db import get_db
from models import Job


async def get_current_job(id: int, db: AsyncSession = Depends(get_db)) -> Job:
    not_found_exception = HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Запрашиваемой вакансии не существует"
    )
    job = await job_queries.get_job_by_id(db=db, id=id)

    if job is None:
        raise not_found_exception

    return job
