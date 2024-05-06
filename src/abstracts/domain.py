import abc


class DomainModel(abc.ABC):
    pass


class AggregateRoot(DomainModel):
    """
    Абстрактный класс для aggregate root
    """
    pass


class Entity(DomainModel):
    """
    Абстрактный класс для entity
    """
    pass


class ValueObject(DomainModel):
    """
    Абстрактный класс для value object
    """
    pass
