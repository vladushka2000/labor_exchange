from dataclasses import dataclass
import uuid

from abstracts.domain import ValueObject


@dataclass
class Response(ValueObject):
    def __init__(self, applicant_id: uuid, message: str) -> None:
        self.applicant_id = applicant_id
        self.message = message
