from datetime import datetime

import factory
from factory_boy_extra.async_sqlalchemy_factory import AsyncSQLAlchemyModelFactory

from models import Job


class JobFactory(AsyncSQLAlchemyModelFactory):
    class Meta:
        model = Job
        # exclude = ['dummy_user_id']

    id = factory.Sequence(lambda n: n)
    # dummy_user_id = factory.SubFactory(UserFactory)
    # user_id = factory.LazyAttribute(lambda o: o.dummy_user_id.id)
    user_id = 0
    title = factory.Faker("pystr", min_chars=10, max_chars=200)
    description = factory.Faker("pystr", min_chars=100, max_chars=200)
    salary_from = factory.Faker("pyint", min_value=16242, max_value=1000000)
    salary_to = factory.Faker("pyint", min_value=salary_from, max_value=1000000)
    is_active = True
    created_at = factory.LazyFunction(datetime.utcnow)
