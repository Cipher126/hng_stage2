import datetime
import aiomysql
import pytz


async def insert_or_update_country(conn, data: dict):
    async with conn.cursor() as cursor:
        query = """
            INSERT INTO countries (
                name, capital, region, population, currency_code,
                exchange_rate, estimated_gdp, flag_url, last_refreshed_at
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                capital = VALUES(capital),
                region = VALUES(region),
                population = VALUES(population),
                currency_code = VALUES(currency_code),
                exchange_rate = VALUES(exchange_rate),
                estimated_gdp = VALUES(estimated_gdp),
                flag_url = VALUES(flag_url),
                last_refreshed_at = VALUES(last_refreshed_at)
        """
        await cursor.execute(query, (
            data["name"],
            data.get("capital"),
            data.get("region"),
            data.get("population"),
            data.get("currency_code"),
            data.get("exchange_rate"),
            data.get("estimated_gdp"),
            data.get("flag_url"),
            datetime.datetime.now(pytz.utc).isoformat(),
        ))
        await conn.commit()


async def get_all_countries(conn):
    async with conn.cursor(aiomysql.DictCursor) as cursor:
        await cursor.execute("SELECT * FROM countries ORDER BY name ASC")
        return await cursor.fetchall()


async def get_country_by_name(conn, name: str):
    async with conn.cursor(aiomysql.DictCursor) as cursor:
        await cursor.execute("SELECT * FROM countries WHERE name = %s", (name,))
        return await cursor.fetchone()


async def get_country_by_region(conn, region: str):
    async with conn.cursor(aiomysql.DictCursor) as cursor:
        await cursor.execute("SELECT * FROM countries WHERE region = %s", (region.title(),))
        return await cursor.fetchall()


async def get_country_sort_by_gdp(conn):
    async with conn.cursor(aiomysql.DictCursor) as cursor:
        await cursor.execute("SELECT * FROM countries ORDER BY estimated_gdp DESC")
        return await cursor.fetchall()


async def get_country_by_currency(conn, currency: str):
    async with conn.cursor(aiomysql.DictCursor) as cursor:
        await cursor.execute("SELECT * FROM countries WHERE currency_code = %s", (currency.upper(),))
        return await cursor.fetchall()


async def delete_country(conn, name: str):
    async with conn.cursor() as cursor:
        await cursor.execute("DELETE FROM countries WHERE name = %s", (name,))
        await conn.commit()
        return cursor.rowcount
