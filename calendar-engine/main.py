from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
from calendars.converter import convert_date

app = FastAPI()

class ConvertDateRequest(BaseModel):
    date: str
    calendar: str = "harptos"

@app.get("/")
def read_root():
    return {"status": "ok"}

@app.post("/convert-date")
def convert_date_endpoint(req: ConvertDateRequest):
    try:
        parsed_date = datetime.strptime(req.date, "%Y-%m-%d").date()
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD.")
    
    result = convert_date(parsed_date, req.calendar)
    return {"converted_date": result}
