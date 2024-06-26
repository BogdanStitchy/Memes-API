import os
from typing import Literal

from dotenv import load_dotenv

load_dotenv("private_media_service/config/.env")

MODE: Literal["DEV", "TEST", "PROD"] = os.environ['MODE']

LOGIN_S3 = os.environ['LOGIN_S3']
PASSWORD_S3 = os.environ['PASSWORD_S3']
HOST_S3 = os.environ['HOST_S3']


