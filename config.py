from dotenv import load_dotenv
import os
load_dotenv()
MODEL=os.getenv("MODEL")
PORT=os.getenv("PORT")
TIMEOUT=os.getenv("TIMEOUT")
LOG_LEVEL=os.getenv("LOG_LEVEL")
