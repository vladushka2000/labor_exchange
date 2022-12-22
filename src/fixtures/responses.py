import factory
from factory_boy_extra.async_sqlalchemy_factory import AsyncSQLAlchemyModelFactory

from models import Response


class ResponseFactory(AsyncSQLAlchemyModelFactory):
    class Meta:
        model = Response

    id = factory.Sequence(lambda n: n)
    user_id = 0
    job_id = 0
    message = factory.Faker("pystr")
