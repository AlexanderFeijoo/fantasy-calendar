from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime

from calendars.converter import convert_date
from calendars.types import CustomCalendarDate

app = FastAPI()


class ConvertDateRequest(BaseModel):
    gregorian: str | None = None
    year: int | None = None
    month: str | None = None
    day: int | None = None
    calendar: str = "harptos"


@app.get("/")
def read_root():
    return {"status": "ok"}


@app.post("/convert-date")
def convert_date_endpoint(req: ConvertDateRequest):
    if req.gregorian:
        try:
            parsed_date = datetime.strptime(req.gregorian, "%Y-%m-%d").date()
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD.")
        result = convert_date(parsed_date, req.calendar)
        return {"calendar_date": result.__dict__}

    if None not in (req.year, req.month, req.day):
        cc_date = CustomCalendarDate(year=req.year, month=req.month, day=req.day)
        try:
            g_date = convert_date(cc_date, req.calendar)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        return {"gregorian_date": g_date.isoformat()}

    raise HTTPException(status_code=400, detail="Provide either 'gregorian' or calendar fields")
