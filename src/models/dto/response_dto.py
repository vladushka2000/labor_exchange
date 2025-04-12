from pydantic import Field

from interfaces import base_dto


class UpdatedResponse(base_dto.BaseDTO):
    """
    Модель обновленных данных для объекта отклика
    """

    message: str = Field(description="Сопроводительное письмо")
