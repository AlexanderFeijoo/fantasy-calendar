from .harptos import HarptosCalendar

# Mapping of supported calendar schemas by slug name
CALENDAR_MAP = {
    "harptos": HarptosCalendar,
}

__all__ = ["CALENDAR_MAP", "HarptosCalendar"]
