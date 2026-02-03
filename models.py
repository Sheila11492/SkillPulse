from dataclasses import dataclass


@dataclass
class Activity:
    date: str
    activity_type: str
    duration: int
    energy: int
    notes: str