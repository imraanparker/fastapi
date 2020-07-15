# -*- coding: utf-8 -*-
from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from app import utils
import fastapi
import datetime
import uvicorn

app = FastAPI()
utils.setup_easter_holidays()

@app.get("/")
def status():
    """ Status check """
    return PlainTextResponse(content="OK")

@app.get("/api/1.0/business_hours")
def calculate_business_hours(start_time: str, end_time: str) -> str:
    """
    Determine the business seconds in a date range. Weekends and South African public holidays are not regarded as business days.
    The dates provided are converted to UTC for comparison. The timezone for each date is taken into consideration during the conversion.
    Only the standard public holidays are taken into consideration. No special holidays that do not repeat from year to year are included.
    The Public Holidays Act, 1994 (https://www.gov.za/sites/default/files/gcis_document/201409/act36of1994.pdf) is used as the standard for all calculations.
    For easter, the Western date is used.
    @param start_time: The start time'
    @param end_time: The end time 
    """
    validation_status_code = fastapi.status.HTTP_422_UNPROCESSABLE_ENTITY

    # validation
    start_date = utils.decode_date(start_time)
    if isinstance(start_date, str):
        return PlainTextResponse(status_code=validation_status_code, content="Start time invalid: %s" % start_date)
    end_date = utils.decode_date(end_time)
    if isinstance(end_date, str):
        return PlainTextResponse(status_code=validation_status_code, content="End time invalid: %s" % end_date)
    start_of_end_day = end_date.replace(hour=0, minute=0, second=0)
    if end_date == start_of_end_day:
        # No time was given with the end date, so setting to the end of the day
        end_date = end_date.replace(hour=utils.BUSINESS_DAY_END, minute=0, second=0)
    error_message = None
    if start_date > end_date:
        error_message =  "The end_time must be greater than the start_time"
    elif start_date.date() < datetime.date(year=utils.START_YEAR, month=1, day=1) or end_date.date() > datetime.date(year=utils.END_YEAR, month=1, day=1):
        error_message =  "The date range must be between the years %s and %s" % (utils.START_YEAR, utils.END_YEAR)
    if error_message:
        return PlainTextResponse(status_code=validation_status_code, content=error_message)

    # work out the seconds 
    total_seconds = 0
    # add the seconds for full days between the start and end date
    next_day = (start_date + datetime.timedelta(days=1)).replace(hour=0, minute=0, second=0)
    difference = start_of_end_day - next_day
    if difference.days > 0:
        total_seconds += difference.days * utils.SECONDS_IN_BUSINESS_DAY

    # deduct if the full days land on a weekend or public holiday
    for full_day in utils.date_range(next_day, end_date):
        if not utils.is_date_in_busines_day(full_day):
            total_seconds -= utils.SECONDS_IN_BUSINESS_DAY

    # add the seconds for the start date
    if utils.is_date_in_busines_day(start_date):
        start_of_day = start_date.replace(hour=utils.BUSINESS_DAY_START, minute=0, second=0)
        end_of_day = start_date.replace(hour=utils.BUSINESS_DAY_END, minute=0, second=0)
        if start_date < start_of_day:
            start_date = start_of_day
        if end_of_day > start_date:
            total_seconds += (end_of_day - start_date).total_seconds()

    # add the seconds for the end date 
    if utils.is_date_in_busines_day(end_date):
        start_of_day = end_date.replace(hour=utils.BUSINESS_DAY_START, minute=0, second=0)
        end_of_day = end_date.replace(hour=utils.BUSINESS_DAY_END, minute=0, second=0)
        if end_date > end_of_day:
            end_date = end_of_day
        if start_of_day < end_date:
            total_seconds += (end_date - start_of_day).total_seconds()

    return PlainTextResponse(content=str(int(total_seconds)))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
