from dataclasses import dataclass


@dataclass
class StudentProfile:
    id: int | None
    name: str
    nim: str
