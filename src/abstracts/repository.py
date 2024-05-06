import abc

from abstracts.domain import DomainModel


class OrmModel:
    """
    Абстрактный класс alchemy_orm-модели.
    """
    pass


class Mapper(abc.ABC):
    @abc.abstractmethod
    def map_orm_to_domain(self, orm_model: OrmModel) -> DomainModel:
        """
        Смапить модель alchemy_orm к доменной модели.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def map_domain_to_orm(self, domain_model: DomainModel) -> OrmModel:
        """
        Смапить доменную модель к alchemy_orm-модели.
        """
        raise NotImplementedError


class Repository(abc.ABC):
    pass
