import uuid

import sqlalchemy as sa
from sqlalchemy.orm import relationship

from abstracts.repository import OrmModel
from repository.alchemy_orm.common import GUID
from repository.alchemy_orm.common import Base


class Response(Base, OrmModel):
    __tablename__ = "responses"

    id = sa.Column(
        GUID(),
        primary_key=True,
        comment="Идентификатор отклика",
        default=lambda: str(uuid.uuid4())
    )
    user_id = sa.Column(GUID(), sa.ForeignKey('users.id'), nullable=False, comment="Идентификатор пользователя")
    job_id = sa.Column(GUID(), sa.ForeignKey('jobs.id'), nullable=False, comment="Идентификатор вакансии")
    message = sa.Column(sa.String, comment="Сопроводительное письмо")
    user = relationship("User", back_populates="responses", lazy="joined")
    job = relationship("Job", back_populates="responses", lazy="joined")
