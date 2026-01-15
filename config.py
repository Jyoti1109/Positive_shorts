# config.py
import os
from dotenv import load_dotenv

load_dotenv()

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")  # ← ADD THIS LINE

if not YOUTUBE_API_KEY:
    raise ValueError("❌ YOUTUBE_API_KEY missing in .env")
if not GROQ_API_KEY:
    raise ValueError("❌ GROQ_API_KEY missing in .env")  # ← Optional but recommended

# MySQL DB Configc
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '12345',  # update if needed
    'database': 'joynews'
}