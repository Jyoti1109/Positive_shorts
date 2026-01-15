# youtube_api.py
import requests
from config import YOUTUBE_API_KEY

def fetch_youtube_shorts(keyword: str, max_results: int = 20):
    # ✅ FIXED: Removed trailing space in URL
    url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        'part': 'snippet',
        'type': 'video',
        'videoDuration': 'short',
        'maxResults': max_results,
        'q': keyword,
        'key': YOUTUBE_API_KEY
    }
    try:
        resp = requests.get(url, params=params, timeout=10)
        resp.raise_for_status()
        return resp.json().get('items', [])
    except Exception as e:
        print(f"⚠️ YouTube Search Error for '{keyword}': {e}")
        return []

def get_video_details(video_id: str):
    # ✅ FIXED: Removed trailing space in URL
    url = "https://www.googleapis.com/youtube/v3/videos"
    params = {
        'part': 'snippet,contentDetails,statistics,status',
        'id': video_id,
        'key': YOUTUBE_API_KEY
    }
    try:
        resp = requests.get(url, params=params, timeout=10)
        resp.raise_for_status()
        items = resp.json().get('items', [])
        return items[0] if items else None
    except Exception as e:
        print(f"⚠️ Video details error for {video_id}: {e}")
        return None

def is_valid_short(duration_iso: str) -> bool:
    import re
    match = re.match(r'PT(?:(\d+)M)?(?:(\d+)S)?', duration_iso)
    if not match:
        return False
    minutes = int(match.group(1)) if match.group(1) else 0
    seconds = int(match.group(2)) if match.group(2) else 0
    total_sec = minutes * 60 + seconds
    return total_sec < 60