import httpx
import asyncio
import logging
import random

from fastapi import HTTPException

from core.config import (
    COUNTRIES_API_URL,
    EXCHANGE_API_URL,
    MIN_GDP_MULTIPLIER,
    MAX_GDP_MULTIPLIER,
)
from core.exception import DataValidationError

logger = logging.getLogger(__name__)


async def fetch_countries_data():
    async with httpx.AsyncClient(timeout=15) as client:
        try:
            response = await client.get(COUNTRIES_API_URL)
            response.raise_for_status()
            countries = response.json()
            logger.info(f"Fetched {len(countries)} countries from RESTCountries API.")
            return countries
        except httpx.RequestError as e:
            logger.error(f"Network error while fetching countries: {e}")
            return []
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error fetching countries: {e}")
            return []


async def fetch_exchange_rates():
    async with httpx.AsyncClient(timeout=15) as client:
        try:
            response = await client.get(EXCHANGE_API_URL)
            response.raise_for_status()
            data = response.json()
            rates = data.get("rates", {})
            logger.info(f"Fetched {len(rates)} exchange rates successfully.")
            return rates
        except httpx.RequestError as e:
            logger.error(f"Network error while fetching exchange rates: {e}")
            return {}
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error fetching exchange rates: {e}")
            return {}


async def merge_country_data():
    countries = await fetch_countries_data()
    rates = await fetch_exchange_rates()

    merged_data = []

    for country in countries:
        try:
            name = country.get("name")
            capital = country.get("capital")
            region = country.get("region")
            population = country.get("population", 0)
            flag_url = country.get("flag")

            if not name:
                logger.warning("Skipping country with missing name.")
                continue

            if not population:
                logger.warning(f"Missing population for {name}, setting GDP to 0.")
                population = 0

            currencies = country.get("currencies", [])

            if not currencies:
                merged_data.append({
                    "name": name,
                    "capital": capital,
                    "region": region,
                    "population": population,
                    "currency_code": None,
                    "exchange_rate": None,
                    "estimated_gdp": 0,
                    "flag_url": flag_url,
                })
                continue

            currency_code = currencies[0].get("code")
            if not currency_code:
                logger.warning(f"{name} has no valid currency code.")
                merged_data.append({
                    "name": name,
                    "capital": capital,
                    "region": region,
                    "population": population,
                    "currency_code": None,
                    "exchange_rate": None,
                    "estimated_gdp": 0,
                    "flag_url": flag_url,
                })
                continue

            exchange_rate = rates.get(currency_code.upper())

            if exchange_rate is None:
                merged_data.append({
                    "name": name,
                    "capital": capital,
                    "region": region,
                    "population": population,
                    "currency_code": currency_code,
                    "exchange_rate": None,
                    "estimated_gdp": 0,
                    "flag_url": flag_url,
                })
                continue

            estimated_gdp = round((
                population * random.uniform(MIN_GDP_MULTIPLIER, MAX_GDP_MULTIPLIER)
            ) / exchange_rate, 1)

            merged_data.append({
                "name": name,
                "capital": capital,
                "region": region,
                "population": population,
                "currency_code": currency_code,
                "exchange_rate": exchange_rate,
                "estimated_gdp": estimated_gdp,
                "flag_url": flag_url,
            })

        except Exception as e:
            logger.warning(f"Skipping country due to data issue: {e}")
            continue

    logger.info(f"Processed {len(merged_data)} valid countries successfully.")
    return merged_data

if __name__ == "__main__":
    asyncio.run(merge_country_data())