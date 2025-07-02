# calendars/harptos_config.py

# =====================
# Calendar Definitions
# =====================

# Harptos months (30 days each)
HARPTOS_MONTHS = [
    "Hammer",      # Deepwinter
    "Alturiak",    # The Claw of Winter
    "Ches",        # The Claw of Sunsets
    "Tarsakh",     # The Claw of Storms
    "Mirtul",      # The Melting
    "Kythorn",     # The Time of Flowers
    "Flamerule",   # Summertide
    "Eleasis",     # Highsun
    "Eleint",      # The Fading
    "Marpenoth",   # Leaffall
    "Uktar",       # The Rotting
    "Nightal"      # The Drawing Down
]

# Number of days in each regular month
DAYS_PER_MONTH = 30

# Special holidays inserted between specific months
INTERCALARY_DAYS = [
    {"name": "Midwinter",        "after": "Hammer",     "day": 31},
    {"name": "Greengrass",       "after": "Tarsakh",    "day": 31},
    {"name": "Midsummer",        "after": "Flamerule",  "day": 31},
    {"name": "Shieldmeet",       "after": "Midsummer",  "day": 32, "leap_year_only": True},  # Every 4 years
    {"name": "Highharvestide",   "after": "Eleint",     "day": 31},
    {"name": "Feast of the Moon","after": "Uktar",      "day": 31}
]

# =====================
# Epoch Configuration
# =====================

# Internally, year 0 STX is 1130 Gregorian
HARPTOS_EPOCH = {
    "gregorian_start": "1130-01-01",  # Corresponds to 1 Hammer, 0 STX
    "harptos_year": 0
}
