import datetime

import sqlalchemy as sa
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import relationship

from db_settings import Base


class Job(Base):
    __tablename__ = "jobs"

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True, comment="Идентификатор вакансии")
    user_id = sa.Column(sa.Integer, sa.ForeignKey('users.id'), comment="Идентификатор пользователя")
    title = sa.Column(sa.String, comment="Название вакансии")
    description = sa.Column(sa.String, comment="Описание вакансии")
    salary_from = sa.Column(sa.Integer, comment="Зарплата от")
    salary_to = sa.Column(sa.Integer, comment="Зарплата до")
    is_active = sa.Column(sa.Boolean, comment="Активна ли вакансия")
    created_at = sa.Column(sa.DateTime, comment="Дата создания записи", default=datetime.datetime.utcnow)
    responses = relationship("Response", back_populates="job")
    jobs = association_proxy("responses", "user")
