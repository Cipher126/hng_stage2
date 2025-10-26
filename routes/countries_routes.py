import os
from fastapi import HTTPException, APIRouter, Depends, Query, Response
from fastapi.responses import FileResponse

from core.config import SUMMARY_IMAGE_PATH
from database.connection import get_db, logger
from services.data_fetcher import merge_country_data
from utils.image_generator import generate_summary_image
from database.model import (insert_or_update_country, get_country_sort_by_gdp, get_country_by_currency,
                            get_country_by_name, get_all_countries, get_country_by_region, delete_country)

router = APIRouter(prefix='/countries', tags=['Countries'])

@router.post('/refresh', status_code=200)
async def refresh(conn=Depends(get_db)):
    try:
        country_data = await merge_country_data()

        if not country_data:
            raise HTTPException(status_code=500, detail="internal server error")

        for country in country_data:
            await insert_or_update_country(conn, country)

        countries = await get_all_countries(conn)
        total_countries = len(countries)

        generate_summary_image(countries)

        logger.info(f"Successfully refreshed {total_countries} countries.")
        return {
            "status": "success",
            "message": f"Refreshed {total_countries} countries successfully.",
            "total_countries": total_countries,
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error during refresh: {e}", exc_info=True)
    raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/image", status_code=200)
async def get_summary_image():
    if not os.path.exists(SUMMARY_IMAGE_PATH):
        raise HTTPException(status_code=404, detail="Summary image not found")

    return FileResponse(
        SUMMARY_IMAGE_PATH,
        media_type="image/png",
        filename="summary.png"
    )

@router.get("", status_code=200)
async def list_countries(
    region: str | None = Query(None),
    currency: str | None = Query(None),
    sort: str | None = Query(None),
    conn=Depends(get_db)
):
    try:
        if region:
            countries = await get_country_by_region(conn, region.title())
        elif currency:
            countries = await get_country_by_currency(conn, currency.upper())
        elif sort and sort.lower() == "gdp_desc":
            countries = await get_country_sort_by_gdp(conn)
        else:
            countries = await get_all_countries(conn)

        if not countries:
            raise HTTPException(status_code=404, detail="Country not found")

        return countries
    except Exception as e:
        logger.error(f"List countries failed: {e}")
        raise HTTPException(status_code=500, detail="internal server error")


@router.get("/{name}", status_code=200)
async def get_country(name: str, conn=Depends(get_db)):
    country = await get_country_by_name(conn, name)
    if not country:
        raise HTTPException(status_code=404, detail="Country not found")
    return country


@router.delete("/{name}", status_code=204)
async def delete_country_by_name(name: str, conn=Depends(get_db)):
    try:
        country = await get_country_by_name(conn, name)

        if not country:
            raise HTTPException(status_code=404, detail="Country not found")

        await delete_country(conn, name)
        return Response(status_code=204)

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail="internal server error")