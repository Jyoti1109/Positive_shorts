import psycopg2
from urllib.parse import urlparse
from config import DATABASE_URL

def get_db_connection():
    url = urlparse(DATABASE_URL)
    conn = psycopg2.connect(
        host=url.hostname,
        port=url.port,
        database=url.path[1:],  # Remove leading '/'
        user=url.username,
        password=url.password,
        sslmode='require'  # Render requires SSL
    )
    return conn

def save_short_to_db(short: dict):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Avoid duplicates
    cursor.execute("SELECT 1 FROM youtube_shorts WHERE video_id = %s", (short['video_id'],))
    if cursor.fetchone():
        conn.close()
        return

    query = """
        INSERT INTO youtube_shorts 
        (video_id, title, description, thumbnail, channel, published_at, views, likes, comments)
        VALUES (%s, %s, %s, %s, %s, %s, %s, % s, %s)
    """
    values = (
        short['video_id'],
        short['title'],
        short['description'],
        short['thumbnail'],
        short['channel'],
        short['published_at'],
        int(short['views']) if short['views'].isdigit() else 0,
        int(short['likes']) if short['likes'].isdigit() else 0,
        int(short['comments']) if short['comments'].isdigit() else 0
    )
    cursor.execute(query, values)
    conn.commit()
    conn.close()