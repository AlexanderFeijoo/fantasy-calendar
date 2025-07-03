from datetime import date, timedelta
from typing import Iterator, Tuple, Union
from dateutil.parser import parse as date_parser
from calendars.schema import CalendarSchema
from calendars.types import CustomCalendarDate
from calendars import CALENDAR_MAP


def _is_leap(year: int, schema: CalendarSchema) -> bool:
    return schema.is_leap_year(year) if schema.is_leap_year else False


def _yield_after(name: str, year: int, schema: CalendarSchema) -> Iterator[Tuple[str, int]]:
    for d in [i for i in schema.intercalary_days if i.after == name]:
        if not d.leap_year_only or _is_leap(year, schema):
            yield (d.name, 1)
            yield from _yield_after(d.name, year, schema)


def _year_iter(year: int, schema: CalendarSchema) -> Iterator[Tuple[str, int]]:
    for m in schema.months:
        for day in range(1, m.days + 1):
            yield (m.name, day)
        yield from _yield_after(m.name, year, schema)


def _year_length(year: int, schema: CalendarSchema) -> int:
    return sum(1 for _ in _year_iter(year, schema))


def _day_index_to_custom(day_index: int, year: int, schema: CalendarSchema) -> CustomCalendarDate:
    for idx, (name, day) in enumerate(_year_iter(year, schema)):
        if idx == day_index:
            return CustomCalendarDate(year=year, month=name, day=day)
    raise ValueError("Day index out of range")


def _custom_to_day_index(cc_date: CustomCalendarDate, schema: CalendarSchema) -> int:
    for idx, (name, day) in enumerate(_year_iter(cc_date.year, schema)):
        if name == cc_date.month and day == cc_date.day:
            return idx
    raise ValueError("Unknown calendar date")


def is_gregorian_leap(year: int) -> bool:
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)


def days_between_gregorian(start: date, end: date) -> int:
    """Calculates day difference between two dates, manually supporting BCE years."""
    reverse = False
    if start > end:
        start, end = end, start
        reverse = True

    total_days = 0
    for year in range(start.year, end.year):
        total_days += 366 if is_gregorian_leap(year) else 365

    total_days += (end - date(end.year, 1, 1)).days
    total_days -= (start - date(start.year, 1, 1)).days

    return -total_days if reverse else total_days


def gregorian_to_calendar(g_date: Union[str, date], schema: CalendarSchema) -> CustomCalendarDate:
    if isinstance(g_date, str):
        g_date = date_parser(g_date).date()

    days = days_between_gregorian(schema.epoch_date, g_date)
    year = schema.epoch_year

    if days >= 0:
        while days >= _year_length(year, schema):
            days -= _year_length(year, schema)
            year += 1
    else:
        while days < 0:
            year -= 1
            days += _year_length(year, schema)

    return _day_index_to_custom(days, year, schema)


def calendar_to_gregorian(cc_date: CustomCalendarDate, schema: CalendarSchema) -> date:
    days = 0
    year = schema.epoch_year
    while year < cc_date.year:
        days += _year_length(year, schema)
        year += 1
    while year > cc_date.year:
        year -= 1
        days -= _year_length(year, schema)

    day_index = _custom_to_day_index(cc_date, schema)
    days += day_index
    return schema.epoch_date + timedelta(days=days)


def convert_date(input_obj: Union[str, date, CustomCalendarDate], calendar: str = "harptos") -> Union[CustomCalendarDate, date]:
    schema = CALENDAR_MAP.get(calendar.lower())
    if not schema:
        raise ValueError(f"Unknown calendar '{calendar}'")

    if isinstance(input_obj, (str, date)):
        return gregorian_to_calendar(input_obj, schema)
    elif isinstance(input_obj, CustomCalendarDate):
        return calendar_to_gregorian(input_obj, schema)
    else:
        raise TypeError("input_obj must be a str, datetime.date, or CustomCalendarDate")
