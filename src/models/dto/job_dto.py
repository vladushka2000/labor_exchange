from pydantic import Field

from interfaces import base_dto


class UpdatedJob(base_dto.BaseDTO):
    """
    Модель обновленных данных для объекта вакансии
    """

    title: str = Field(description="Название вакансии")
    description: str = Field(description="Описание вакансии")
    salary_from: int = Field(description="Зарплата от")
    salary_to: int = Field(description="Зарплата до")
    is_active: bool = Field(description="Флаг активности вакансии")
