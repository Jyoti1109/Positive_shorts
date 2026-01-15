# db.py
import mysql.connector
from config import DB_CONFIG

def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)

def save_short_to_db(short: dict):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Avoid duplicates
    cursor.execute("SELECT 1 FROM youtube_shorts WHERE video_id = %s", (short['video_id'],))
    if cursor.fetchone():
        conn.close()
        return  # Skip duplicate

    query = """
        INSERT INTO youtube_shorts 
        (video_id, title, description, thumbnail, channel, published_at, views, likes, comments)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    values = (
        short['video_id'],
        short['title'],
        short['description'],
        short['thumbnail'],
        short['channel'],
        short['published_at'],
        short['views'],
        short['likes'],
        short['comments']
    )
    cursor.execute(query, values)
    conn.commit()
    conn.close()