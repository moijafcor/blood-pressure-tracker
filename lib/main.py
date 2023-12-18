""" 
A tracker program for monitoring blood pressure readings.

This program allows users to record and track their blood pressure readings. 
It provides an interactive mode where users can enter new readings, 
plot the table of existing readings, plot a chart of the readings, or quit the program. 
It also supports non-interactive mode where readings can be recorded directly using command-line arguments.

Usage:
    python main.py [-h] [-t {night,morning}] [-s SYSTOLIC] [-d DIASTOLIC]

Options:
    -h, --help              Show this help message and exit.
    -t, --time              Time of day for the blood pressure reading. Defaults to 'morning'.
    -s, --systolic          Systolic blood pressure reading.
    -d, --diastolic         Diastolic blood pressure reading.

Environment Variables:
    EXCEL_FILE_PATH         Path to the Excel file for storing the blood pressure readings.

Version: 1.0.0
"""

import os
import sys
from dotenv import load_dotenv
import argparse
import pandas as pd
import gnureadline
from datetime import datetime
from lib.bp_handler import record_blood_pressure, print_table, plot_blood_pressure
from lib.bp_reading_payload import BloodPressureReadingPayload
from lib.bp_mode_interactive_morning import bp_morning
from lib.bp_mode_interactive_night import bp_night

# Load environment variables from .env file
load_dotenv()

VERSION = "1.0.0"


def main(
    interactive: bool = True,
    systolic: int = None,
    diastolic: int = None,
    comments: str = None,
    time_of_day: str = None,
):
    """
    Main function of the blood pressure tracker program.

    Args:
        interactive (bool): Flag indicating whether to run in interactive mode. Defaults to True.
        systolic (int): Systolic blood pressure reading. Only used in non-interactive mode.
        diastolic (int): Diastolic blood pressure reading. Only used in non-interactive mode.
        time_of_day (str): Time of day for the blood pressure reading. Defaults to 'morning'.
                            Only used in non-interactive mode.
        excel_file_path (str): Path to the Excel file for storing the blood pressure readings.
    Returns:
        None
    """

    try:
        excel_file_path = os.environ.get("EXCEL_FILE_PATH")
        if excel_file_path is None:
            raise ValueError("Excel file path not specified.")
    except ValueError as e:
        print(e)
        sys.exit(1)

    if interactive:
        print(f"Simple Blood Pressure Tracker (v.{ VERSION }) ")
        while True:
            print(
                "Enter '1' log morning reading, "
                "'2' log night reading, "
                "'3' plot table, "
                "'4' plot morning chart, "
                "'5' plot night chart, "
                "or 'x' to quit."
            )
            action = input()

            if action == "1":
                bp_morning()
            elif action == "2":
                bp_night()
            elif action == "3":
                print_table(excel_file_path=excel_file_path)
            elif action == "4":
                plot_blood_pressure(
                    excel_file_path=excel_file_path, time_of_day="morning"
                )
            elif action == "5":
                plot_blood_pressure(
                    excel_file_path=excel_file_path, time_of_day="night"
                )
            elif action.lower() == "x":
                print("Bye!")
                break
            else:
                print("Invalid option. Please enter '1', '2', '3', '4', '5', or 'x'.")
    else:
        p = BloodPressureReadingPayload(
            morning_systolic=systolic if time_of_day == "morning" else 0,
            morning_diastolic=diastolic if time_of_day == "morning" else 0,
            night_systolic=systolic if time_of_day == "night" else 0,
            night_diastolic=diastolic if time_of_day == "night" else 0,
            timestamp=datetime.now(),
            time_of_day=time_of_day,
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
