from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from enum import Enum
from datetime import date
from typing import Optional

from calendars.converter import convert_date
from calendars.types import CustomCalendarDate

class CalendarName(str, Enum):
    harptos = "harptos"

class CalendarDate(BaseModel):
    year: int
    month: str
    day: int

class ConvertDateRequest(BaseModel):
    gregorian: Optional[str] = None
    year: Optional[int] = None
    month: Optional[str] = None
    day: Optional[int] = None
    calendar: CalendarName = CalendarName.harptos

class ConvertDateResponse(BaseModel):
    calendar_date: Optional[CalendarDate] = None
    gregorian_date: Optional[date] = None

app = FastAPI()

# Allow local frontend during development
origins = ["http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"status": "ok"}

@app.post("/convert-date", response_model=ConvertDateResponse)
def convert_date_endpoint(req: ConvertDateRequest):
    if req.gregorian:
        try:
            result = convert_date(req.gregorian, req.calendar)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        return {"calendar_date": result.__dict__}

    if None not in (req.year, req.month, req.day):
        cc_date = CustomCalendarDate(year=req.year, month=req.month, day=req.day)
        try:
            g_date = convert_date(cc_date, req.calendar)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        return {"gregorian_date": g_date}

    raise HTTPException(status_code=400, detail="Provide either 'gregorian' or calendar fields")
