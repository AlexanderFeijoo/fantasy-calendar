from datetime import date

def convert_date(input_date: date, calendar: str = "harptos") -> str:
    if calendar.lower() == "harptos":
        # Placeholder —
        return "1 HAMMER 700 STX"
    else:
        # Fallback: return ISO format as human-readable
        return input_date.strftime("%B %d, %Y")
