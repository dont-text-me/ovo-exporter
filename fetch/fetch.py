import asyncio
import httpx
import logging
import datetime
import itertools
from datetime import timedelta
from shared import url_utils
from shared.reading import Reading
from shared.environment import get_ovo_username, get_ovo_password, get_account_number
from shared.url_utils import LOGOUT_URL

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
logging.getLogger("httpx").disabled = True


async def fetch_last_three_days():
    async with httpx.AsyncClient() as client:
        await client.post(
            url_utils.LOGIN_URL,
            json={
                "username": get_ovo_username(),
                "password": get_ovo_password(),
                "rememberMe": True,
            },
        )
        auth_response = await client.get(url_utils.AUTH_URL)
        access_token = auth_response.json()["accessToken"]["value"]
        three_day_stats = await asyncio.gather(
            *[
                _get_readings(
                    client,
                    access_token,
                    get_account_number(),
                    datetime.datetime.now() - timedelta(days=d),
                )
                for d in range(1, 4)
            ],
        )
        three_day_stats = list(itertools.chain.from_iterable(three_day_stats))
        logger.info(f"Found {len(three_day_stats)} readings over the last 3 days")
        await client.get(LOGOUT_URL)
        return three_day_stats


async def _get_readings(client, access_token, account_number, date):
    url = url_utils.build_usage_request(account_number, date)
    headers = {"Authorization": f"Bearer {access_token}"}
    data_response = await client.get(url, headers=headers)
    if data_response.status_code != 200:
        logger.warning(
            f"Error fetching readings for {date.date()}, status code: {data_response.status_code}"
        )
        return []
    readings = [
        Reading.from_json(r) for r in data_response.json()["electricity"]["data"]
    ]
    logger.info(f"Found {len(readings)} readings for {date.date()}")
    return readings
