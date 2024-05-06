from abstracts.repository import Mapper
from domain.job import Job as DomainJob
from domain.job.value_objects import Response as DomainResponse, Salary as DomainSalary
from repository.alchemy_orm.models import Job as OrmJob, Response as OrmResponse


class JobMapper(Mapper):
    @staticmethod
    def map_orm_to_domain(orm_model: OrmJob) -> DomainJob:
        def _map_salary(job_model: OrmJob) -> DomainSalary:
            return DomainSalary(
                salary_from=job_model.salary_from,
                salary_to=job_model.salary_to
            )

        def _map_response(response_model: OrmResponse) -> DomainResponse:
            return DomainResponse(
                applicant_id=response_model.user_id,
                message=response_model.message
            )

        return DomainJob(
            job_id=orm_model.id,
            company_id=orm_model.user_id,
            title=orm_model.title,
            description=orm_model.description,
            salary=_map_salary(orm_model),
            is_active=orm_model.is_active,
            responses=[_map_response(response) for response in orm_model.responses]
        )

    @staticmethod
    def map_domain_to_orm(domain_model: DomainJob) -> OrmJob:
        def _map_response(response_model: DomainResponse) -> OrmResponse:
            return OrmResponse(
                user_id=response_model.applicant_id,
                job_id=domain_model.job_id,
                message=response_model.message
            )

        return OrmJob(
            id=domain_model.job_id,
            user_id=domain_model.company_id,
            title=domain_model.title,
            description=domain_model.description,
            salary_from=domain_model.salary.salary_from,
            salary_to=domain_model.salary.salary_to,
            is_active=domain_model.is_active,
            created_at=domain_model.created_at,
            responses=[
                _map_response(response) for response in domain_model.responses
            ]
        )
