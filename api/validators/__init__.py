# Dictonary to save internal String identifier
from calendar import Calendar

from .student_employee import StudentEmployeeValidator

VALIDATOR_CLASS_NAMES = (
    ("studEmp", "Studentische Hilfskraft"),
    ("regEmp", "Regulär*er Angestelt*er"),
    ("civilSer", "Beamt*in"),
)

FTE_WEEKYL_MINUTES = {
    "regEmp": 2400,  # 40h per week
    "civilSer": 2460,  # 41h per week
}
VALIDATOR_CLASSES = {"studEmp": StudentEmployeeValidator}


def calculate_business_days(date, start_day=0, end_day=31):
    """
    Claculate the number of business days in the given month.
    :param: date
    """
    weeks_in_month = Calendar().monthdayscalendar(date.year, date.month)
    day_count = 0
    for week in weeks_in_month:
        day_count += sum(map(lambda x: start_day < x <= end_day, week[:5]))
    return day_count


def business_weeks(date, start_day=0, end_day=31):
    """
    Provide the number of business weeks (5 days in a business week) for a given
    month as float.
    """
    return calculate_business_days(date, start_day, end_day) / 5


def worktime_multiplicator(current_date, start_date, end_date, month_end_day):
    end_day = month_end_day
    if end_date.month == current_date.month and end_date.year == current_date.year:
        end_day = end_date.day
    # -1 needed to count the start date too
    return business_weeks(current_date, start_date.day - 1, end_day)


def stud_emp_worktime_multiplicator(current_date, start_date, end_date, month_end_day):
    if start_date.month == current_date.month and start_date.year == current_date.year:
        return (month_end_day - start_date.day + 1) / month_end_day
    if end_date.month == current_date.month and end_date.year == current_date.year:
        return end_date.day / month_end_day
    return 1
