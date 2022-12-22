import factory

from models import Job
from datetime import datetime
from factory_boy_extra.async_sqlalchemy_factory import AsyncSQLAlchemyModelFactory


class JobFactory(AsyncSQLAlchemyModelFactory):
    class Meta:
        model = Job
        # exclude = ['dummy_user_id']

    id = factory.Sequence(lambda n: n)
    # dummy_user_id = factory.SubFactory(UserFactory)
    # user_id = factory.LazyAttribute(lambda o: o.dummy_user_id.id)
    user_id = 0
    title = factory.Faker("pystr")
    description = factory.Faker("pystr")
    salary_from = factory.Faker("pyint")
    salary_to = factory.Faker("pyint")
    is_active = True
    created_at = factory.LazyFunction(datetime.utcnow)
