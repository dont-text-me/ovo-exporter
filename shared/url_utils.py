import datetime

LOGIN_URL = "https://my.ovoenergy.com/api/v2/auth/login"
LOGOUT_URL = "https://my.ovoenergy.com/api/auth/logout"
AUTH_URL = "https://my.ovoenergy.com/api/v2/auth/token"
HALF_HOURLY_USAGE_URL = "https://smartpaymapi.ovoenergy.com/usage/api/half-hourly"


def build_usage_request(account_number: str, date: datetime.datetime):
    return f"{HALF_HOURLY_USAGE_URL}/{account_number}?date={date.date().isoformat()}"
