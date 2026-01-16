from flask import Flask, render_template, jsonify
from flask_cors import CORS
import os  # ← जोडले

app = Flask(__name__)
CORS(app)

@app.after_request
def add_csp_headers(response):
    # 🔥 FIXED: trailing spaces in CSP removed
    response.headers['Content-Security-Policy'] = (
        "default-src 'self'; "
        "script-src 'self' 'unsafe-inline' https://www.youtube.com https://s.ytimg.com https://www.google.com; "
        "frame-src 'self' https://www.youtube.com; "
        "connect-src 'self'; "
        "style-src 'self' 'unsafe-inline'; "
        "img-src 'self' data: https://i.ytimg.com; "
        "media-src 'self' https://www.youtube.com; "
        "object-src 'none'; "
        "base-uri 'self'; "
        "form-action 'self'; "
        "frame-ancestors 'self'; "
        "upgrade-insecure-requests;"
    )
    return response

from db import get_db_connection
import threading
import time

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/shorts')
def get_shorts():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM youtube_shorts ORDER BY published_at DESC LIMIT 50")
    shorts = cursor.fetchall()
    conn.close()

    for s in shorts:
        vid = s['video_id']
        # 🔥 FIXED: NO TRAILING SPACES in URLs
        s['embed_url'] = (
            f"https://www.youtube.com/embed/{vid}"
            f"?autoplay=1&mute=1&controls=0&modestbranding=1&rel=0"
            f"&loop=1&playlist={vid}&playsinline=1&enablejsapi=1"
        )
        s['watch_url'] = f"https://youtu.be/{vid}"  # ✅ Clean URL
    
    return jsonify(shorts)

@app.route('/fetch-and-store-shorts', methods=['POST'])
def trigger_fetch():
    from ingest_shorts import collect_positive_shorts
    collect_positive_shorts()
    return jsonify({"status": "success", "message": "Shorts fetched and stored!"})

def auto_fetch_shorts():
    while True:
        print("🔄 Auto-fetching fresh positive shorts...")
        try:
            from ingest_shorts import collect_positive_shorts
            collect_positive_shorts()
            print("✅ Auto-fetch completed!")
        except Exception as e:
            print(f"❌ Auto-fetch error: {e}")
        time.sleep(86400)

fetch_thread = threading.Thread(target=auto_fetch_shorts, daemon=True)
fetch_thread.start()

if __name__ == '__main__':
    print("🚀 Starting JoyScroll - Positive Shorts Platform")
    # 🔧 Step 3: PORT support for Render + local dev
    port = int(os.environ.get("PORT", 5000)) 
    print(f"👉 Visit http://localhost:{port} or http://192.168.1.37:{port}")
    app.run(debug=False, host='0.0.0.0', port=port)  # ← port=port