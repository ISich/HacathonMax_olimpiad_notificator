import os
from dotenv import load_dotenv

load_dotenv()

MAX_TOKEN = os.getenv("MAX_TOKEN")
MAX_BASE_URL = "https://platform-api2.max.ru"

DATABASE_URL = os.getenv("DATABASE_URL")
TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL")

if not MAX_TOKEN:
    raise ValueError("MAX_TOKEN не найден в .env")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL не найден в .env")