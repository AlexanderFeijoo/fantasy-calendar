# Fantasy Calendar

A full-stack calendar web app for tracking and managing custom fantasy-world calendars, inspired by **Dungeons & Dragons' Calendar of Harptos**. This project includes a Dockerized FastAPI backend engine and a Prisma/PostgreSQL schema designed to eventually power a rich Next.js frontend UI.

---

## Features (Working Today)

- Bi-directional date conversion between **Gregorian** and **custom calendars** like Harptos
- Full Docker-based local development setup with FastAPI + PostgreSQL
- Schema support for leap years, intercalary holidays, and year epochs
- Working `/convert-date` API endpoint (via FastAPI)
- Full unit test suite for conversion logic
- Custom calendar logic modeled using extensible Python classes
- Prisma schema defined for calendars, events, and characters

---

## Project Structure

```
fantasy-calendar/
├── docker-compose.yml         # Orchestrates services (FastAPI, Postgres, future frontend)
├── .env                       # Environment config for Postgres, ports, etc.
├── README.md                  # This file
│
├── prisma/                    # Prisma ORM setup for Postgres
│   ├── schema.prisma          # Models: Event, Calendar, Character, etc.
│   └── client/                # Generated Prisma client (checked into Git for now)
│
├── frontend/                  # (WIP) Next.js frontend
│   ├── pages/                 # Dynamic calendar views (future)
│   ├── components/            # UI building blocks (Tailwind + Radix planned)
│   └── ...
│
├── calendar-engine/           # Python FastAPI microservice for calendar conversions
│   ├── main.py                # `/convert-date` endpoint (FastAPI)
│   ├── converter.py           # Core conversion logic (Gregorian <-> fantasy)
│   ├── requirements.txt       # Python deps (installed locally for linting)
│   ├── Dockerfile             # Container for the service
│   │
│   ├── calendars/
│   │   ├── schema.py          # `CalendarSchema`, `Month`, `IntercalaryDay` classes
│   │   ├── types.py           # `CustomCalendarDate` struct (used in API and logic)
│   │   ├── harptos.py         # Harptos calendar schema definition
│   │   └── __init__.py
│   │
│   ├── tests/
│   │   └── test_converter.py  # Unit tests for conversion logic (Pytest)
│   └── ...
│
└── scripts/                   # (Optional) CLI utilities, seed data scripts
```

---

## Running Locally with Docker

### Prerequisites

- Docker + Docker Compose
- Python (optional, for local linting/testing)
- Node.js (optional, frontend WIP)

### Setup Steps

```bash
git clone https://github.com/AlexanderFeijoo/fantasy-calendar.git
cd fantasy-calendar

# Generate the Prisma client (output will be created in `prisma/client`)
npx prisma generate

# Install Python dependencies locally (for editor linting)
cd calendar-engine
pip install -r requirements.txt

# Start everything with Docker
cd ..
docker compose up --build
```

The FastAPI service will be available at [http://localhost:5001](http://localhost:5001)

---

## Running Tests

Tests run inside the Docker container using Pytest:

```bash
docker compose run --rm test
```

To install and run tests locally:

```bash
cd calendar-engine
pip install -r requirements.txt
pytest
```

---

## API: `/convert-date`

POST `/convert-date` accepts either:

- A **Gregorian** date to convert into a fantasy calendar:
  ```json
  {
    "gregorian": "1132-07-31",
    "calendar": "harptos"
  }
  ```

- A **fantasy calendar** date to convert into Gregorian:
  ```json
  {
    "year": 2,
    "month": "Shieldmeet",
    "day": 1,
    "calendar": "harptos"
  }
  ```

Returns:
```json
{
  "calendar_date": {
    "year": 2,
    "month": "Midsummer",
    "day": 1
  }
}
```

---

## Supported Calendar: Harptos

- 12 months of 30 days
- Intercalary holidays: Midwinter, Greengrass, Midsummer, etc.
- Shieldmeet (leap-year-only day)
- Harptos year 0 = Gregorian 1130

Leap year logic aligns with Gregorian via the calendar epoch.

---

## Architectural Notes

- **Gregorian** is the canonical date format internally (used for DB storage)
- All conversions happen relative to the **calendar schema epoch**
- Users select which calendar to view; conversion occurs at display time
- **Calendar schemas** can be added via Python classes using `CalendarSchema`

---

## Roadmap

Planned features:

- Frontend UI (Next.js + Tailwind + Radix)
- Auth + session support
- Full CRUD for events, notes, characters
- Repeat rules (e.g. lunar cycles, holidays)
- Multiple calendars per campaign
- Host via AWS (FastAPI Lambda + RDS)
- Admin interface for custom calendar definitions

## 

---

## Dev Tips

- `.env` defines DB connection details for Prisma + Postgres
- Prisma generates client code into `prisma/client` (run `npx prisma generate` to create it)
- Use `pip install -r requirements.txt` locally for editor linting
- All new calendar systems should subclass `CalendarSchema` for clean integration

---

## About the Project

This is a senior-level portfolio project intended to demonstrate:

- Modular full-stack architecture
- Custom date conversion engines
- API design + validation
- Infrastructure as code (Docker)
- Clean separation of core logic and schemas

---

© 2025 Alexander Feijoo — Built for DMs, worldbuilders, and nerds everywhere.
