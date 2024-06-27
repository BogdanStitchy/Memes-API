import os
from typing import Literal

from dotenv import load_dotenv

load_dotenv("public_memes_api/config/.env")

MODE: Literal["DEV", "TEST", "PROD"] = os.environ['MODE']
LOG_LEVEL = os.environ['LOG_LEVEL']

DRIVER_DB = "asyncpg"
DIALECT_DB = "postgresql"

LOGIN_DB = os.environ['LOGIN_DB']
PASSWORD_DB = os.environ['PASSWORD_DB']
NAME_DB = os.environ['NAME_DB']
HOST = os.environ['HOST']
DB_PORT = os.environ['DB_PORT']


TEST_LOGIN_DB = os.environ['TEST_LOGIN_DB']
TEST_PASSWORD_DB = os.environ['TEST_PASSWORD_DB']
TEST_NAME_DB = os.environ['TEST_NAME_DB']
TEST_HOST = os.environ['TEST_HOST']
TEST_PORT = os.environ['TEST_PORT']


PRIVATE_MEDIA_SERVICE_URL = os.environ['PRIVATE_MEDIA_SERVICE_URL']

DATABASE_URL = f"{DIALECT_DB}+{DRIVER_DB}://{LOGIN_DB}:{PASSWORD_DB}@{HOST}:{DB_PORT}/{NAME_DB}"
TEST_DATABASE_URL = f"{DIALECT_DB}+{DRIVER_DB}://{TEST_LOGIN_DB}:{TEST_PASSWORD_DB}@{TEST_HOST}:{TEST_PORT}/{TEST_NAME_DB}"


