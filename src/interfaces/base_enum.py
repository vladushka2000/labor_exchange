from __future__ import annotations  # no qa

import enum
import uuid


class ReferenceEnum(enum.Enum):
    """
    Базовыйп Enum для объектов, содержащих идентификатор и название
    """

    def __new__(cls, id_: uuid.UUID | int, name: str) -> ReferenceEnum:
        """
        Инициализировать объект
        :param id_: идентификатор поля справочника
        :param name: название
        :return: объект Enum
        """

        obj = object().__new__(cls)
        obj._value_ = (id_, name)
        obj.id_ = id_
        obj.name_ = name

        return obj

    @classmethod
    def get_by_id(cls, id_: uuid.UUID | int) -> ReferenceEnum | None:
        """
        Получить элемент по id_
        :param id_: идентификатор
        :return: элемент или None, если не найден
        """

        for member in cls:
            if member.id_ == id_:
                return member

        return None

    @classmethod
    def get_by_name(cls, name: str) -> ReferenceEnum | None:
        """
        Получить элемент по name_
        :param name: название
        :return: элемент или None, если не найден
        """

        for member in cls:
            if member.name_ == name:
                return member

        return None
