import uuid

from abstracts.domain import AggregateRoot
from .value_objects import PersonalInfo


class User(AggregateRoot):
    def __init__(
        self,
        user_id: uuid,
        personal_info: PersonalInfo,
        hashed_password: int,
        jobs: list[uuid]
    ) -> None:
        self.user_id = user_id
        self.personal_info = personal_info
        self.hashed_password = hashed_password
        self.jobs = jobs
