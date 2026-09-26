from dataclasses import dataclass
from datetime import datetime


@dataclass
class OlympiadStage:
    id: int
    olympiad_id: int

    name: str

    start_at: datetime
    end_at: datetime