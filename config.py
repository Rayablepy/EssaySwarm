import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).with_name(".env"))

MODEL = os.getenv("MODEL")
PORT = int(os.getenv("PORT", 8000))
TIMEOUT = int(os.getenv("TIMEOUT", 1800))
LOG_LEVEL = os.getenv("LOG_LEVEL", "info")
