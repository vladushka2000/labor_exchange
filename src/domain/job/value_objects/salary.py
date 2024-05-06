from dataclasses import dataclass

from abstracts.domain import ValueObject


@dataclass
class Salary(ValueObject):
    def __init__(self, salary_from: int, salary_to: int) -> None:
        self.salary_from = salary_from
        self.salary_to = salary_to
