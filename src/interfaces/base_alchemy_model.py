from typing import Any, Iterable

from sqlalchemy.ext.declarative import declarative_base

AlchemyBase = declarative_base()


class ActiveRecord:
    """
    Интерфейс модели
    """

    def create(self, *args, **kwargs) -> Any:
        """
        Создать запись
        """

        raise NotImplementedError

    def retrieve(self, *args, **kwargs) -> Any:
        """
        Получить запись
        """

        raise NotImplementedError

    def list(self, *args, **kwargs) -> Iterable[Any]:
        """
        Получить список записей
        """

        raise NotImplementedError

    def update(self, *args, **kwargs) -> Any:
        """
        Обновить запись
        """

        raise NotImplementedError

    def delete(self, *args, **kwargs) -> Any:
        """
        Удалить запись
        """

        raise NotImplementedError
