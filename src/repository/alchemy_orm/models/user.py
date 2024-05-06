import datetime
import uuid

import sqlalchemy as sa
from sqlalchemy.orm import relationship

from abstracts.repository import OrmModel
from repository.alchemy_orm.common import GUID
from repository.alchemy_orm.common import Base


class User(Base, OrmModel):
    __tablename__ = "users"

    id = sa.Column(
        GUID(),
        primary_key=True,
        comment="Идентификатор пользователя",
        default=lambda: str(uuid.uuid4())
    )
    email = sa.Column(sa.String, comment="Email адрес", unique=True)
    name = sa.Column(sa.String, comment="Имя пользователя")
    hashed_password = sa.Column(sa.String, comment="Зашифрованный пароль")
    is_company = sa.Column(sa.Boolean, comment="Флаг компании")
    created_at = sa.Column(sa.DateTime, comment="Время создания записи", default=datetime.datetime.utcnow)
    jobs = relationship("Job", back_populates="user", lazy="joined")
    responses = relationship("Response", back_populates="user", lazy="joined")
