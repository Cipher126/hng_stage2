from fastapi import Depends, FastAPI, APIRouter, HTTPException
from database.connection import get_db
from database.model import get_all_countries

status = APIRouter(prefix='/status', tags=['Status'])

@status.get("")
async def get_status(conn=Depends(get_db)):
    countries = await get_all_countries(conn)
    if not countries:
        raise HTTPException(status_code=404, detail="No data found")

    total = len(countries)
    last_refreshed = max(
        (c["last_refreshed_at"] for c in countries if c["last_refreshed_at"]), default=None
    )

    return {
        "total_countries": total,
        "last_refreshed_at": last_refreshed,
    }