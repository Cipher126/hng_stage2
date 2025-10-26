import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME")

DATABASE_URL = (
    f"mysql+aiomysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

COUNTRIES_API_URL = "https://restcountries.com/v2/all?fields=name,capital,region,population,flag,currencies"
EXCHANGE_API_URL = "https://open.er-api.com/v6/latest/USD"

CACHE_DIR = Path(__file__).resolve().parent.parent / "cache"
SUMMARY_IMAGE_PATH = CACHE_DIR / "summary.png"

MIN_GDP_MULTIPLIER = 1000
MAX_GDP_MULTIPLIER = 2000
DEFAULT_EXCHANGE_BASE = "USD"

CACHE_DIR.mkdir(parents=True, exist_ok=True)
