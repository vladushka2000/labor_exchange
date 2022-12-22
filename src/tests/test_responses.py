import pytest
from fastapi import HTTPException

from fixtures.jobs import JobFactory
from fixtures.responses import ResponseFactory
from fixtures.users import UserFactory
from queries import response as response_query
from schemas.responses import ResponseInSchema


@pytest.mark.asyncio
async def test_get_my_responses_as_user(sa_session):
    user = UserFactory.build(is_company=False)
    sa_session.add(user)
    await sa_session.flush()

    job = JobFactory.build()
    job.user_id = user.id
    sa_session.add(job)
    await sa_session.flush()

    response = ResponseFactory.build()
    response.user_id = user.id
    response.job_id = job.id
    sa_session.add(response)
    await sa_session.flush()

    all_responses = await response_query.get_my_responses(db=sa_session, current_user=user)

    assert all_responses
    assert len(all_responses) == 1
    assert all_responses[0] == response


@pytest.mark.asyncio
async def test_get_my_responses_as_company(sa_session):
    user = UserFactory.build(is_company=False)
    sa_session.add(user)
    await sa_session.flush()

    company = UserFactory.build(is_company=True)
    sa_session.add(user)
    await sa_session.flush()

    job = JobFactory.build()
    job.user_id = user.id
    sa_session.add(job)
    await sa_session.flush()

    response = ResponseFactory.build()
    response.user_id = user.id
    response.job_id = job.id
    sa_session.add(response)
    await sa_session.flush()

    with pytest.raises(HTTPException) as http_exception:
        await response_query.get_my_responses(db=sa_session, current_user=company)

    assert http_exception.value.status_code == 403
    assert http_exception.value.detail == "Компания не может делать отклики на вакансии"


@pytest.mark.asyncio
async def test_get_responses_by_job_id(sa_session):
    user = UserFactory.build(is_company=False)
    sa_session.add(user)
    await sa_session.flush()

    job = JobFactory.build()
    job.user_id = user.id
    sa_session.add(job)
    await sa_session.flush()

    response = ResponseFactory.build()
    response.user_id = user.id
    response.job_id = job.id
    sa_session.add(response)
    await sa_session.flush()

    all_responses = await response_query.get_responses_by_job_id(db=sa_session, id=job.id)

    assert all_responses
    assert len(all_responses) == 1
    assert all_responses[0] == response


@pytest.mark.asyncio
async def test_create_response_by_user(sa_session):
    user = UserFactory.build(is_company=False)
    sa_session.add(user)
    await sa_session.flush()

    job = JobFactory.build()
    job.user_id = user.id
    sa_session.add(job)
    await sa_session.flush()

    response = ResponseInSchema(
        job_id=job.id,
        message="берите меня"
    )

    new_response = await response_query.create_response(sa_session, response_schema=response, current_user=user)

    assert new_response is not None
    assert new_response.job_id == response.job_id
    assert new_response.message == response.message


@pytest.mark.asyncio
async def test_create_response_by_company(sa_session):
    user = UserFactory.build(is_company=True)
    sa_session.add(user)
    await sa_session.flush()

    job = JobFactory.build()
    job.user_id = user.id
    sa_session.add(job)
    await sa_session.flush()

    response = ResponseInSchema(
        job_id=job.id,
        message="берите меня"
    )

    with pytest.raises(HTTPException) as http_exception:
        await response_query.create_response(sa_session, response_schema=response, current_user=user)

    assert http_exception.value.status_code == 403
    assert http_exception.value.detail == "Компания не может делать отклики на вакансии"
