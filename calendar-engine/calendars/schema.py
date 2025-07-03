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
    after: str                  # Month it follows
    leap_year_only: bool = False

@dataclass
class CalendarSchema:
    name: str
    epoch_date: date
    epoch_year: int
    months: List[Month]
    intercalary_days: List[IntercalaryDay]
    is_leap_year: Optional[Callable[[int], bool]] = None
    has_fixed_year_length: bool = True
