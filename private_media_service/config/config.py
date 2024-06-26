import os
from typing import Literal

from dotenv import load_dotenv

load_dotenv("private_media_service/config/.env")

MODE: Literal["DEV", "TEST", "PROD"] = os.environ['MODE']

LOGIN_S3 = os.environ['LOGIN_DB']
PASSWORD_S3 = os.environ['PASSWORD_DB']
HOST_S3 = os.environ['HOST']


