# test_db.py
from config import DB_CONFIG
import mysql.connector

try:
    conn = mysql.connector.connect(**DB_CONFIG)
    print("✅ Successfully connected to MySQL!")
    conn.close()
except Exception as e:
    print("❌ DB Connection Failed:", e)