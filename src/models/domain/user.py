from __future__ import annotations  # noqa

import datetime
import uuid
from sqlalchemy.orm import Mapped, mapped_column

from interfaces import base_alchemy_model


class User(base_alchemy_model.AlchemyBase, base_alchemy_model.ActiveRecord):
    """
    Модель пользователя
    """

    __tablename__ = "user"
    __table_args__ = {"comment": "Пользователи"}

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, default=uuid.uuid4, comment="Идентификатор пользователя"
    )
    email: Mapped[str] = mapped_column(comment="Email-адрес", unique=True)
    username: Mapped[str] = mapped_column(comment="Username")
    first_name: Mapped[str] = mapped_column(comment="Имя")
    last_name: Mapped[str] = mapped_column(comment="Фамилия")
    created_at: Mapped[datetime.datetime] = mapped_column(
        comment="Дата регистрации", nullable=True
    )
