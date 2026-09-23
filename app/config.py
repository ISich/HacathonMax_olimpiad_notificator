import os
from dotenv import load_dotenv

load_dotenv()

MAX_TOKEN = os.getenv("MAX_TOKEN")
MAX_BASE_URL = "https://platform-api2.max.ru"

if not MAX_TOKEN:
    raise ValueError("MAX_TOKEN не найден в .env")