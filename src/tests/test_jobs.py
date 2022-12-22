import pytest
from fastapi import HTTPException

from fixtures.jobs import JobFactory
from fixtures.users import UserFactory
from queries import job as job_query
from schemas.jobs import JobInSchema, JobUpdateSchema


@pytest.mark.asyncio
async def test_get_all_jobs(sa_session):
    user = UserFactory.build()
    sa_session.add(user)
    await sa_session.flush()

    job = JobFactory.build()
    job.user_id = user.id
    sa_session.add(job)
    await sa_session.flush()

    all_jobs = await job_query.get_all_jobs(sa_session)
    assert all_jobs
    assert len(all_jobs) == 1
    assert all_jobs[0] == job


@pytest.mark.asyncio
async def test_get_job(sa_session):
    user = UserFactory.build()
    sa_session.add(user)
    await sa_session.flush()

    job = JobFactory.build()
    job.user_id = user.id
    sa_session.add(job)
    await sa_session.flush()

    current_job = await job_query.get_job_by_id(sa_session, job.id)
    assert current_job is not None
    assert current_job.id == job.id


@pytest.mark.asyncio
async def test_create_job_by_company(sa_session):
    user = UserFactory.build(is_company=True)
    sa_session.add(user)
    await sa_session.flush()

    job = JobInSchema(
        title="Kassir",
        description="Na kasse",
        salary_from=0,
        salary_to=123,
        is_active=True
    )

    new_job = await job_query.create_job(sa_session, job_schema=job, current_user=user)

    assert new_job is not None
    assert new_job.title == job.title
    assert new_job.description == job.description
    assert new_job.salary_from == job.salary_from
    assert new_job.salary_to == job.salary_to
    assert new_job.is_active


@pytest.mark.asyncio
async def test_create_job_by_non_company(sa_session):
    user = UserFactory.build(is_company=False)
    sa_session.add(user)
    await sa_session.flush()

    job = JobInSchema(
        title="Kassir",
        description="Na kasse",
        salary_from=0,
        salary_to=123,
        is_active=True
    )

    with pytest.raises(HTTPException) as http_exception:
        await job_query.create_job(sa_session, job_schema=job, current_user=user)

    assert http_exception.value.status_code == 403
    assert http_exception.value.detail == "Пользователь не имеет прав :("


@pytest.mark.asyncio
async def test_update_job_by_related_user(sa_session):
    user = UserFactory.build(is_company=True)
    sa_session.add(user)
    await sa_session.flush()

    job = JobFactory.build()
    job.user_id = user.id
    sa_session.add(job)
    await sa_session.flush()

    updated_job = JobUpdateSchema(
        title="updated_kassir",
        description="updated_rabota_na_kasse",
        salary_from=123,
        salary_to=246,
        is_active=False
    )

    updated_job = await job_query.update_job(sa_session, job=job, updated_job=updated_job, current_user=user)

    assert job.id == updated_job.id
    assert job.title == updated_job.title
    assert job.description == updated_job.description
    assert job.salary_from == updated_job.salary_from
    assert job.salary_to == updated_job.salary_to
    assert job.is_active == updated_job.is_active


@pytest.mark.asyncio
async def test_update_job_by_unrelated_user(sa_session):
    user_related = UserFactory.build(is_company=True)
    sa_session.add(user_related)
    await sa_session.flush()

    user_unrelated = UserFactory.build()
    sa_session.add(user_unrelated)
    await sa_session.flush()

    job = JobFactory.build()
    job.user_id = user_related.id
    sa_session.add(job)
    await sa_session.flush()

    updated_job = JobUpdateSchema(
        title="updated_kassir",
        description="updated_rabota_na_kasse",
        salary_from=123,
        salary_to=246,
        is_active=False
    )

    with pytest.raises(HTTPException) as http_exception:
        await job_query.update_job(sa_session, job=job, updated_job=updated_job, current_user=user_unrelated)

    assert http_exception.value.status_code == 403
    assert http_exception.value.detail == "Это не ты разместил вакансию"