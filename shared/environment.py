import os


def get_ovo_username():
    return os.environ["OVO_USERNAME"]


def get_ovo_password():
    return os.environ["OVO_PASSWORD"]


def get_db_url():
    return os.environ["DATABASE_URL"]


def get_account_number():
    return os.environ["ACCOUNT_NUMBER"]
