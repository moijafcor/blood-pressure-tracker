""" A tracker program for monitoring blood pressure readings. """
import os
import sys
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import pytz
from lib.bp_reading_payload import BloodPressureReadingPayload


def record_blood_pressure(
    p: BloodPressureReadingPayload,
    excel_file_path: str,
    timezone: str,
    date_format: str,
):
    """
    Records the blood pressure readings and updates an Excel file with the new data.

    Args:
        p (BloodPressureReadingPayload): The blood pressure reading payload.
        excel_file_path (str): The file path of the Excel file.

    Returns:
        pd.DataFrame: The updated data containing the blood pressure readings.
    """

    # Get the current date and time in the configured timezone
    timezone = pytz.timezone(timezone)
    current_datetime = datetime.now(timezone)

    # Create a DataFrame with the new readings
    log_data = pd.DataFrame(
        {
            "Date": [current_datetime.strftime(date_format)],
            "Morning Systolic": [int(p.morning_systolic or 0)],
            "Morning Diastolic": [int(p.morning_diastolic or 0)],
            "Night Systolic": [int(p.night_systolic or 0)],
            "Night Diastolic": [int(p.night_diastolic or 0)],
            "Comments": [str(p.comments)],
            "Timestamp": [current_datetime.strftime("%Y-%m-%d %H:%M:%S")],
        }
    )

    try:
        # Try to read the existing Excel file
        existing_data = pd.read_excel(excel_file_path)
        # Append the new readings to the existing data
        updated_data = pd.concat([existing_data, log_data], ignore_index=True)
    except FileNotFoundError:
        # If the file doesn't exist, create a new DataFrame
        primed_data = pd.DataFrame(
            {
                "Date": [current_datetime.strftime(os.environ.get("DATE_FORMAT"))],
                "Morning Systolic": [int(p.morning_systolic or 0)],
                "Morning Diastolic": [int(p.morning_diastolic or 0)],
                "Night Systolic": [int(p.night_systolic or 0)],
                "Night Diastolic": [int(p.night_diastolic or 0)],
                "Comments": [str(p.comments)],
                "Timestamp": [current_datetime.strftime("%Y-%m-%d %H:%M:%S")],
            }
        )
        updated_data = primed_data
        print(f"Excel file not found at { excel_file_path }. Creating a new one...")

    # Write the updated data to the Excel file
    updated_data.to_excel(excel_file_path, index=False)
    print(
        f"{p.time_of_day.capitalize()} blood pressure readings recorded successfully on {current_datetime}"
    )

    return updated_data


def print_table(excel_file_path: str):
    """
    Prints the contents of an Excel file as a table.

    Args:
        excel_file_path (str): The path to the Excel file.

    Raises:
        ValueError: If the Excel file does not exist or if it is empty.

    Returns:
        None
    """

    try:
        if not os.path.exists(excel_file_path):
            raise ValueError(
                "No data repository found. Please log some readings first. Bye!"
            )
        data = pd.read_excel(excel_file_path)
        if data.empty:
            print("No data to display.")
        else:
            print(data)
    except ValueError as e:
        print(e)
        sys.exit(1)


def plot_blood_pressure(excel_file_path: str, time_of_day: str):
    """
    Plots the blood pressure values over time.

    Args:
        excel_file_path (str): The path to the Excel file containing the blood pressure data.
        time_of_day (str): The time of day for which to plot the blood pressure values.

    Raises:
        ValueError: If the specified Excel file does not exist or if it is empty.

    Returns:
        None
    """
    try:
        if not os.path.exists(excel_file_path):
            raise ValueError(
                "No data repository found. Please log some readings first. Bye!"
            )
        data = pd.read_excel(excel_file_path)
        if data.empty:
            raise ValueError(
                "No data repository found. Please log some readings first. Bye!"
            )

        data.set_index("Date", inplace=True)

        # Plotting systolic and diastolic values over time
        if (
            f"{time_of_day.capitalize()} Systolic" in data.columns
            and f"{time_of_day.capitalize()} Diastolic" in data.columns
        ):
            plt.plot(
                data.index,
                data[f"{time_of_day.capitalize()} Systolic"],
                label=f"{time_of_day.capitalize()} Systolic",
                marker="o",
            )
            plt.plot(
                data.index,
                data[f"{time_of_day.capitalize()} Diastolic"],
                label=f"{time_of_day.capitalize()} Diastolic",
                marker="o",
            )

        # Plotting reference lines for normal blood pressure values
        plt.axhline(
            y=120, color="green", linestyle="--", label="Normal Systolic (ACCF/AHA)"
        )
        plt.axhline(
            y=80, color="cyan", linestyle="--", label="Normal Diastolic (ACCF/AHA)"
        )
        plt.axhline(
            y=135,
            color="crimson",
            linestyle="--",
            label="Normal Systolic (Gov of Canada)",
        )
        plt.axhline(
            y=85,
            color="chocolate",
            linestyle="--",
            label="Normal Diastolic (Gov of Canada)",
        )

        plt.title(f"{time_of_day.capitalize()} Blood Pressure Over Time")
        plt.xlabel("Reading Dates")
        plt.ylabel("Blood Pressure (mmHg)")
        plt.ylim(60, 200)  # Set y-axis limits
        plt.legend()

        # Format x-axis timestamps to be more human-readable
        plt.xticks(rotation=45, ha="right")

        plt.tight_layout()
        plt.show()
    except ValueError as e:
        print(e)
        sys.exit(1)
    except Exception as e:
        print(e)
        sys.exit(1)
