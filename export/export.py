import datetime
import logging
import psycopg

from shared.reading import Reading
from shared.environment import get_db_url

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("psycopg")
logger.setLevel(logging.INFO)


def export_readings(readings: list[Reading]):
    with psycopg.connect(get_db_url()) as conn:
        logger.info("DB connection successful")
        with conn.cursor() as cursor:
            cursor.executemany(
                """
            INSERT INTO half_hourly_electricity_reading
            (interval_start, interval_end, consumption, unit)
            VALUES (%s, %s, %s, %s) ON CONFLICT DO NOTHING
            """,
                _to_rows(readings),
            )
            logger.info(f"Inserted {cursor.rowcount} readings")


def _to_rows(readings: list[Reading]):
    return [
        (r.interval_start, r.interval_end, r.consumption, r.unit.lower())
        for r in readings
    ]
