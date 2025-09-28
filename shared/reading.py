from dataclasses import dataclass
from datetime import datetime


@dataclass
class Reading:
    interval_start: datetime
    interval_end: datetime
    consumption: float
    unit: str

    @classmethod
    def from_json(cls, json):
        return Reading(
            interval_start=json["interval"]["start"],
            interval_end=json["interval"]["end"],
            consumption=json["consumption"],
            unit=json["unit"],
        )
