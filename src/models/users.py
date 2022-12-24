import datetime

import sqlalchemy as sa
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import relationship

from db_settings import Base


class User(Base):
    __tablename__ = "users"

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True, comment="Идентификатор задачи", unique=True)
    email = sa.Column(sa.String, comment="Email адрес", unique=True)
    name = sa.Column(sa.String, comment="Имя пользователя")
    hashed_password = sa.Column(sa.String, comment="Зашифрованный пароль")
    is_company = sa.Column(sa.Boolean, comment="Флаг компании")
    created_at = sa.Column(sa.DateTime, comment="Время создания записи", default=datetime.datetime.utcnow)
    responses = relationship("Response", back_populates="user")
    jobs = association_proxy("responses", "job")
