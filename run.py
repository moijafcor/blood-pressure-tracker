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

import argparse
from lib.main import main


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="main.py",
        description="A logger program for recording blood pressure readings.",
        epilog="Pass no arguments in order to use Interactive Mode.",
    )
    parser.add_argument(
        "-t",
        "--time",
        type=str,
        default="morning",
        choices=["night", "morning"],
        help="Time of day for the blood pressure reading. Defaults to 'morning'.",
    )
    parser.add_argument(
        "-n",
        "--comments",
        type=str,
        default=None,
        help="Additional commentss for the blood pressure reading.",
    )
    parser.add_argument(
        "-s",
        "--systolic",
        type=int,
        help="Systolic blood pressure reading.",
    )
    parser.add_argument(
        "-d",
        "--diastolic",
        type=int,
        help="Diastolic blood pressure reading.",
    )
    args = parser.parse_args()
    if args.systolic is None or args.diastolic is None:
        main(interactive=True)
    else:
        main(
            interactive=False,
            systolic=args.systolic,
            diastolic=args.diastolic,
            comments=args.comments,
            time_of_day=args.time,
        )
