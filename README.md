# fantasy-calendar

This repository contains a small FastAPI service for converting between the
Gregorian calendar and custom calendar schemas. The included engine currently
supports the Forgotten Realms **Calendar of Harptos**.

Run the API:

```bash
cd calendar-engine
uvicorn main:app
```

Example requests:

- Convert a Gregorian date to a calendar date:
  ```json
  {"gregorian": "1132-07-31"}
  ```
- Convert back to Gregorian:
  ```json
  {"year": 2, "month": "Shieldmeet", "day": 1}
  ```

The `tests/` directory contains unit tests showing sample conversions.
