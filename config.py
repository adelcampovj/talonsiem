import os
from dotenv import load_dotenv

load_dotenv()

THRESHOLD = int(os.getenv("THRESHOLD", 5))
WINDOW_SECONDS = int(os.getenv("WINDOW_SECONDS", 60))

EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", 587))
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER")
