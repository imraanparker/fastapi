# -*- coding: utf-8 -*-
import datetime
import dateutil.parser

START_YEAR = 1582
END_YEAR = 3100
SATURDAY = 5
SUNDAY = 6
BUSINESS_DAY_START = 8
BUSINESS_DAY_END = 17
SECONDS_IN_BUSINESS_DAY = 32400

# Each public holiday is the day, month. So 21 March is (21, 3)
ZA_HOLIDAYS = [(1, 1), (21, 3), (27, 4), (1, 5), (16, 6), (9, 8), (24, 9), (16, 12), (25, 12), (26, 12)]
EASTER_HOLIDAYS = list()


def setup_easter_holidays():
    """
    Create the dictionary of easter holidays
    """
    for y in range(START_YEAR, END_YEAR+1):
        easter = calculate_western_easter(y)
        easter_friday = easter - datetime.timedelta(days=2)
        easter_monday = easter + datetime.timedelta(days=1)
        EASTER_HOLIDAYS.extend((easter_friday, easter_monday))

def calculate_western_easter(year: int) -> datetime:
    """
    Returns easter as a date object.
    @param year: The year to calculate easter
    @return: The date of easter sunday
    """
    a = year % 19 # golden year
    b = year // 100 # century
    c = year % 100
    # Epact
    d = (19 * a + b - b // 4 - ((b - (b + 8) // 25 + 1) // 3) + 15) % 30
    # weekday for Paschal Full Moon (0=Sunday)
    e = (32 + 2 * (b % 4) + 2 * (c // 4) - d - (c % 4)) % 7
    # number of days from March 21 to Sunday on or before Paschal Full Moon
    f = d + e - 7 * ((a + 11 * d + 22 * e) // 451) + 114
    month = f // 31
    day = f % 31 + 1
    return datetime.date(year, month, day)

def decode_date(iso_date: str) -> datetime:
    """
    Decodes the ISO date to a datetime object.
    @param iso_date: The ISO date.
    @return: The datetime object or None if the date could not be decoded
    """
    try:
        v = dateutil.parser.isoparse(iso_date)
        if v.utcoffset():
            v = v - v.utcoffset()
        return v.replace(microsecond=0, tzinfo=datetime.timezone.utc)
    except Exception as e:
        return str(e)

def date_range(start_date: datetime, end_date: datetime) -> datetime:
    """
    Returns a generator of datetimes to iterate over a date range
    @param start_date: The start date
    @param end_date: The end date
    @return: datetime generator  
    """
    for n in range((end_date - start_date).days):
        yield start_date + datetime.timedelta(days=n)

def is_date_in_busines_day(date_to_check: datetime) -> bool:
    """"
    Checks if a date is part of a business day. Weekends and ZA public holidays are not business days.
    @param date_to_check: The date to check
    @return: Whether to exclude the date or not
    """
    previous_day = date_to_check - datetime.timedelta(days=1)
    current_day_tuple = (date_to_check.day, date_to_check.month)
    previous_day_tuple = (previous_day.day, previous_day.month)
    if current_day_tuple in ZA_HOLIDAYS or (previous_day.weekday() == SUNDAY and previous_day_tuple in ZA_HOLIDAYS):
        return False
    if date_to_check.weekday() in (SATURDAY, SUNDAY):
        return False
    if date_to_check.date() in EASTER_HOLIDAYS:
        return False
    return True
