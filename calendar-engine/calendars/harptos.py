# calendars/harptos.py

from datetime import date
from .schema import CalendarSchema, Month, IntercalaryDay


def harptos_leap_year(year: int) -> bool:
    """Return True if the given Harptos year is a leap year."""
    # Align leap years with the Gregorian cycle so that year 2 (1132) is leap
    return (year + 1130) % 4 == 0


HarptosCalendar = CalendarSchema(
    name="harptos",
    epoch_date=date(1130, 1, 1),  # 1 Hammer, Year 0
    epoch_year=0,
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
        IntercalaryDay("Midwinter", "Hammer", 31),
        IntercalaryDay("Greengrass", "Tarsakh", 31),
        IntercalaryDay("Midsummer", "Flamerule", 31),
        IntercalaryDay("Shieldmeet", "Midsummer", 32, leap_year_only=True),
        IntercalaryDay("Highharvestide", "Eleint", 31),
        IntercalaryDay("Feast of the Moon", "Uktar", 31),
    ],
    is_leap_year=harptos_leap_year,
    has_fixed_year_length=True
)
