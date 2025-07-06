from dataclasses import dataclass
from datetime import date
from typing import Iterator, Tuple, Union
import re
from calendars.schema import CalendarSchema
from calendars.types import CustomCalendarDate
from calendars import CALENDAR_MAP


@dataclass
class ProlepticDate:
    year: int
    month: int
    day: int


DATE_RE = re.compile(r"^(?P<year>-?\d+)-(?P<month>\d{2})-(?P<day>\d{2})$")


def parse_gregorian(date_str: str) -> ProlepticDate:
    match = DATE_RE.match(date_str)
    if not match:
        raise ValueError("Invalid date format. Use YYYY-MM-DD")
    year = int(match.group("year"))
    month = int(match.group("month"))
    day = int(match.group("day"))
    if not 1 <= month <= 12:
        raise ValueError("Month must be in 1..12")
    if day < 1 or day > 31:
        raise ValueError("Day out of range")
    return ProlepticDate(year, month, day)


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


def days_before_year(year: int) -> int:
    y = year - 1
    return y * 365 + y // 4 - y // 100 + y // 400


DAYS_BEFORE_MONTH = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334, 365]
DAYS_BEFORE_MONTH_LEAP = [0, 31, 60, 91, 121, 152, 182, 213, 244, 274, 305, 335, 366]


def _to_ordinal(pdate: ProlepticDate) -> int:
    days = days_before_year(pdate.year)
    days_before_month = DAYS_BEFORE_MONTH_LEAP if is_gregorian_leap(pdate.year) else DAYS_BEFORE_MONTH
    days += days_before_month[pdate.month - 1]
    days += pdate.day
    return days


def days_between_gregorian(start: ProlepticDate, end: ProlepticDate) -> int:
    """Calculates day difference between two Gregorian dates (supports BCE)."""
    start_ord = _to_ordinal(start)
    end_ord = _to_ordinal(end)
    return end_ord - start_ord


def _from_ordinal(n: int) -> date:
    """Convert ordinal day count (1-based) to datetime.date. Supports year>=1."""
    y = (10000 * n + 14780) // 3652425
    while True:
        year_ordinal_start = days_before_year(y + 1) + 1
        if n < year_ordinal_start:
            break
        y += 1

    day_of_year = n - days_before_year(y)
    leap = is_gregorian_leap(y)
    days_before = DAYS_BEFORE_MONTH_LEAP if leap else DAYS_BEFORE_MONTH
    month = 1
    while month <= 12 and day_of_year > days_before[month]:
        month += 1
    day = day_of_year - days_before[month - 1]

    if y <= 0:
        raise ValueError("Gregorian dates before year 1 are not supported")
    return date(y, month, day)


def gregorian_to_calendar(g_date: Union[str, date], schema: CalendarSchema) -> CustomCalendarDate:
    if isinstance(g_date, str):
        parsed = parse_gregorian(g_date)
    elif isinstance(g_date, date):
        parsed = ProlepticDate(g_date.year, g_date.month, g_date.day)
    else:
        raise TypeError("g_date must be a str or date")

    epoch_pd = ProlepticDate(schema.epoch_date.year, schema.epoch_date.month, schema.epoch_date.day)

    days = days_between_gregorian(epoch_pd, parsed)
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

    epoch_pd = ProlepticDate(schema.epoch_date.year, schema.epoch_date.month, schema.epoch_date.day)
    target_ord = _to_ordinal(epoch_pd) + days
    return _from_ordinal(target_ord)


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