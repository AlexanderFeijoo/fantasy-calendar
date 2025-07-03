from datetime import date
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

def test_negative_harptos_year_to_gregorian():
    cc = CustomCalendarDate(year=-5, month="Hammer", day=1)
    result = convert_date(cc)
    assert result == date(1125, 1, 1)


def test_negative_gregorian_to_harptos():
    result = convert_date(date(1125, 1, 1))
    assert result == CustomCalendarDate(year=-5, month="Hammer", day=1)

def test_gregorian_leap_years():
    assert convert_date(date(2000, 2, 29)).day == 29  # 2000 is a leap year
    result = convert_date(date(1900, 3, 1))
    assert result.month == "Alturiak"
    assert result.day == 29  # 1900 is not a leap year, so this is the 29th day of Alturiak

def test_intercalary_boundaries():
    # Day before Greengrass = Tarsakh 30
    before = convert_date(date(1130, 5, 1))
    assert before.month == "Tarsakh"
    assert before.day == 30

    # Greengrass
    greengrass = convert_date(date(1130, 5, 2))
    assert greengrass.month == "Greengrass"

    # Day after Greengrass = Mirtul 1
    after = convert_date(date(1130, 5, 3))
    assert after.month == "Mirtul"
    assert after.day == 1

def test_bce_gregorian_to_harptos():
    result = convert_date("-0200-01-01")
    assert result == CustomCalendarDate(year=-1330, month="Hammer", day=1)




