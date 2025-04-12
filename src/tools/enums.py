import uuid

from interfaces import base_enum


class UserRole(base_enum.ReferenceEnum):
    """
    Enum ролей пользователя
    """

    APPLICANT = (uuid.UUID("0d1846ae-5da5-4814-a76e-813f3a09d978"), "applicant")
    COMPANY = (uuid.UUID("da269c83-9689-4959-94eb-56cf6b48c681"), "company")
    ADMIN = (uuid.uuid4(), "admin")
