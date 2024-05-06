import datetime as dt
import uuid

from abstracts.domain import AggregateRoot
from .value_objects import Response, Salary


class Job(AggregateRoot):
    def __init__(
        self,
        job_id: uuid,
        company_id: uuid,
        title: str,
        description: str,
        salary: Salary,
        is_active: bool,
        responses: list[Response]
    ) -> None:
        self.job_id = job_id
        self.company_id = company_id
        self.title = title
        self.description = description
        self.salary = salary
        self.is_active: bool = is_active
        self.responses = responses
        self.created_at: dt.datetime = dt.datetime.now()

    def add_response(self, applicant_id: uuid, message: str) -> None:
        response = Response(
            applicant_id=applicant_id,
            message=message
        )
        self.responses.append(response)
