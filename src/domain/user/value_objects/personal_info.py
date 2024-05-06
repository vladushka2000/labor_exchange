from dataclasses import dataclass

from abstracts.domain import ValueObject


@dataclass
class PersonalInfo(ValueObject):
    def __init__(self, email: str, name: str) -> None:
        self.email = email
        self.name = name
