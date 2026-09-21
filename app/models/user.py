from dataclasses import dataclass


@dataclass
class User:
    user_id: int
    grade: int | None = None