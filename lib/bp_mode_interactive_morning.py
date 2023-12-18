import os
import sys
from dotenv import load_dotenv
import argparse
import pandas as pd
import gnureadline
from datetime import datetime
from lib.bp_handler import record_blood_pressure
from lib.bp_reading_payload import BloodPressureReadingPayload

# Load environment variables from .env file
load_dotenv()


def bp_morning():
    """
    Interactive mode for recording the morning blood pressure readings.

    Args:
        None

    Returns:
        None
    """
    systolic_min = int(os.environ.get("SYSTOLIC_MIN"))
    systolic_max = int(os.environ.get("SYSTOLIC_MAX"))
    diastolic_min = int(os.environ.get("DIASTOLIC_MIN"))
    diastolic_max = int(os.environ.get("DIASTOLIC_MAX"))
    excel_file_path = os.environ.get("EXCEL_FILE_PATH")

    while True:
        try:
            systolic = input(
                "Please enter your morning systolic blood pressure reading: "
            )
            if systolic.lower() == "x":
                print("Bye!")
                sys.exit(0)
            if systolic.isdigit():
                systolic = int(systolic)
            else:
                raise ValueError()
            if systolic_min <= systolic <= systolic_max:
                break
            raise ValueError()
        except ValueError:
            print(
                f"Invalid systolic blood pressure reading. Please enter a value between {systolic_min} and {systolic_max} or 'q' to quit."
            )
            continue
    while True:
        try:
            diastolic = input(
                "Please enter your morning diastolic blood pressure reading: "
            )

            if diastolic.lower() == "x":
                print("Bye!")
                sys.exit(0)
            if diastolic.isdigit():
                diastolic = int(diastolic)
            else:
                raise ValueError()
            if diastolic_min <= diastolic <= diastolic_max:
                break
            raise ValueError()
        except ValueError:
            print(
                f"Invalid diastolic blood pressure reading. Please enter a value between {diastolic_min} and {diastolic_max} or 'q' to quit."
            )
            continue

    comments = input("Please enter a note (optional): ")
    p = BloodPressureReadingPayload(
        morning_systolic=systolic,
        morning_diastolic=diastolic,
        night_systolic=None,
        night_diastolic=None,
        timestamp=datetime.now(),
        time_of_day="morning",
        comments=comments,
    )

    # Get the current date and time in the configured timezone
    timezone = os.environ.get("TIMEZONE")
    date_format = os.environ.get("DATE_FORMAT")

    record_blood_pressure(
        excel_file_path=excel_file_path,
        p=p,
        timezone=timezone,
        date_format=date_format,
    )
