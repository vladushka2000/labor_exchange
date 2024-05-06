import datetime as dt
import uuid

import sqlalchemy as sa
from sqlalchemy.orm import relationship

from abstracts.repository import OrmModel
from repository.alchemy_orm.common import GUID
from repository.alchemy_orm.common import Base


class Job(Base, OrmModel):
    __tablename__ = "jobs"

    id = sa.Column(
        GUID(),
        primary_key=True,
        comment="Идентификатор вакансии",
        default=lambda: str(uuid.uuid4())
    )
    user_id = sa.Column(GUID(), sa.ForeignKey('users.id'), comment="Идентификатор пользователя")
    title = sa.Column(sa.String, comment="Название вакансии")
    description = sa.Column(sa.String, comment="Описание вакансии")
    salary_from = sa.Column(sa.Integer, comment="Зарплата от")
    salary_to = sa.Column(sa.Integer, comment="Зарплата до")
    is_active = sa.Column(sa.Boolean, comment="Активна ли вакансия")
    created_at = sa.Column(sa.DateTime, comment="Дата создания записи", default=dt.datetime.now())
    user = relationship("User", back_populates="jobs", lazy="joined")
    responses = relationship("Response", back_populates="job", lazy="joined")
