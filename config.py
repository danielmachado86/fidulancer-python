"""Configutarion variables

"""

import os

from dotenv import load_dotenv

load_dotenv()
basedir = os.path.abspath(os.path.dirname(__file__))


def as_bool(value):
    """_summary_

    Args:
        value (_type_): _description_

    Returns:
        _type_: _description_
    """
    if value:
        return value.lower() in ["true", "yes", "on", "1"]
    return False


class Config:
    """Config class"""

    # security options
    SECRET_KEY = os.environ.get("SECRET_KEY", "top-secret!")
    DISABLE_AUTH = as_bool(os.environ.get("DISABLE_AUTH"))
    ACCESS_TOKEN_MINUTES = int(os.environ.get("ACCESS_TOKEN_MINUTES") or "15")
    REFRESH_TOKEN_DAYS = int(os.environ.get("REFRESH_TOKEN_DAYS") or "30")
    REFRESH_TOKEN_IN_COOKIE = as_bool(
        os.environ.get("REFRESH_TOKEN_IN_COOKIE") or "yes"
    )
    REFRESH_TOKEN_IN_BODY = as_bool(os.environ.get("REFRESH_TOKEN_IN_BODY"))
    RESET_TOKEN_MINUTES = int(os.environ.get("RESET_TOKEN_MINUTES") or "15")
    PASSWORD_RESET_URL = (
        os.environ.get("PASSWORD_RESET_URL") or "http://localhost:3000/reset"
    )
    USE_CORS = as_bool(os.environ.get("USE_CORS") or "yes")
    CORS_SUPPORTS_CREDENTIALS = (True,)
    MONGO_URL = os.environ.get("MONGO_URL") or "mongodb"
    MONGO_PORT = int(os.environ.get("MONGO_PORT") or "27017")
    MONGO_USER = os.environ.get("MONGO_USER") or "root"
    MONGO_PASSWORD = os.environ.get("MONGO_PASSWORD") or "example"
    MONGO_DATABASE = os.environ.get("MONGO_DATABASE") or "fidulancer"
    PAYMENT_API_URL = os.environ.get("PAYMENT_API_URL") or "https://sandbox.wompi.co/v1"
    PAYMENT_API_PUBLIC_KEY = os.environ.get("PAYMENT_API_PUBLIC_KEY") or "fake_payment_public_key"
    PAYMENT_API_PRIVATE_KEY = os.environ.get("PAYMENT_API_PRIVATE_KEY") or "fake_payment_private_key"