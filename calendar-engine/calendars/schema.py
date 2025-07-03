from dataclasses import dataclass
from datetime import date
from typing import List, Optional, Callable

@dataclass
class Month:
    name: str
    days: int

@dataclass
class IntercalaryDay:
    name: str
    after: str  # Month name it follows
    day: int    # Absolute day number in the year
    leap_year_only: bool = False

@dataclass
class CalendarSchema:
    name: str
    epoch_date: date         # Gregorian anchor date
    epoch_year: int          # Calendar's internal year at epoch
    months: List[Month]      # Ordered list of calendar months
    intercalary_days: List[IntercalaryDay]
    is_leap_year: Optional[Callable[[int], bool]] = None
    has_fixed_year_length: bool = True
