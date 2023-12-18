from dataclasses import dataclass
from datetime import datetime


@dataclass
class BloodPressureReadingPayload:
    """
    Represents a blood pressure reading payload.

    Attributes:
        morning_systolic (int): The systolic blood pressure reading in the morning.
        morning_diastolic (int): The diastolic blood pressure reading in the morning.
        night_systolic (int): The systolic blood pressure reading at night.
        night_diastolic (int): The diastolic blood pressure reading at night.
        timestamp (datetime): The timestamp of the blood pressure reading.
        time_of_day (str): The time of day when the reading was taken.
        comments (str, optional): Additional comments about the reading.
    """

    morning_systolic: int
    morning_diastolic: int
    night_systolic: int
    night_diastolic: int
    timestamp: datetime
    time_of_day: str
    comments: str = ""
