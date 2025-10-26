import aiomysql
import asyncio
import logging
from core.config import DB_USER, DB_HOST, DB_NAME, DB_PORT, DB_PASSWORD

logger = logging.getLogger(__name__)


async def get_db():
    conn = await aiomysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        db=DB_NAME,
        port=int(DB_PORT)
    )
    try:
        yield conn
    finally:
        conn.close()


async def create_table():
    conn = await aiomysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        db=DB_NAME,
        port=int(DB_PORT)
    )
    try:
        async with conn.cursor() as cursor:
            await cursor.execute("""
                CREATE TABLE IF NOT EXISTS countries (
                    id INT AUTO_INCREMENT UNIQUE,
                    name VARCHAR(100) NOT NULL PRIMARY KEY,
                    capital VARCHAR(100),
                    region VARCHAR(100),
                    population BIGINT NOT NULL,
                    currency_code VARCHAR(10),
                    exchange_rate FLOAT,
                    estimated_gdp DOUBLE,
                    flag_url TEXT,
                    last_refreshed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
                )
            """)
            await conn.commit()
            logger.info("Table 'countries' created successfully.")
    except Exception as e:
        logger.error(f"Exception occurred in create_table: {e}", exc_info=True)
    finally:
        conn.close()


if __name__ == "__main__":
    asyncio.run(create_table())
