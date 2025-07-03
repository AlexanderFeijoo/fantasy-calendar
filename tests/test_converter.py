import os
import sys
from datetime import date

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'calendar-engine'))

from calendars.converter import convert_date
from calendars.types import CustomCalendarDate


def test_gregorian_to_harptos_epoch():
    result = convert_date(date(1130, 1, 1))
    assert result == CustomCalendarDate(year=0, month="Hammer", day=1)


def test_harptos_to_gregorian_epoch():
    cc = CustomCalendarDate(year=0, month="Hammer", day=1)
    result = convert_date(cc)
    assert result == date(1130, 1, 1)


def test_leap_year_midsummer_and_shieldmeet():
    midsummer = convert_date(date(1132, 7, 31))
    assert midsummer == CustomCalendarDate(year=2, month="Midsummer", day=1)

    shieldmeet = convert_date(date(1132, 8, 1))
    assert shieldmeet == CustomCalendarDate(year=2, month="Shieldmeet", day=1)

    back = convert_date(shieldmeet)
    assert back == date(1132, 8, 1)
