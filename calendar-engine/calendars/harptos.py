from datetime import date
from .schema import CalendarSchema, Month, IntercalaryDay


def make_harptos_leap_year(epoch_year: int, epoch_date: date):
    def harptos_leap_year(year: int) -> bool:
        gregorian_year = epoch_date.year + (year - epoch_year)
        return gregorian_year % 4 == 0 and (gregorian_year % 100 != 0 or gregorian_year % 400 == 0)
    return harptos_leap_year


EPOCH_DATE = date(1130, 1, 1)
EPOCH_YEAR = 0

HarptosCalendar = CalendarSchema(
    name="harptos",
    epoch_date=EPOCH_DATE,
    epoch_year=EPOCH_YEAR,
    months=[
        Month("Hammer", 30),
        Month("Alturiak", 30),
        Month("Ches", 30),
        Month("Tarsakh", 30),
        Month("Mirtul", 30),
        Month("Kythorn", 30),
        Month("Flamerule", 30),
        Month("Eleasis", 30),
        Month("Eleint", 30),
        Month("Marpenoth", 30),
        Month("Uktar", 30),
        Month("Nightal", 30),
    ],
    intercalary_days=[
        IntercalaryDay("Midwinter", "Hammer"),
        IntercalaryDay("Greengrass", "Tarsakh"),
        IntercalaryDay("Midsummer", "Flamerule"),
        IntercalaryDay("Shieldmeet", "Midsummer", leap_year_only=True),
        IntercalaryDay("Highharvestide", "Eleint"),
        IntercalaryDay("Feast of the Moon", "Uktar"),
    ],
    is_leap_year=make_harptos_leap_year(EPOCH_YEAR, EPOCH_DATE),
    has_fixed_year_length=True
)
