# ingest_shorts.py — OPTIMIZED VERSION
from youtube_api import fetch_youtube_shorts, get_video_details, is_valid_short
from filter import is_positive_with_groq
from db import save_short_to_db
from datetime import datetime

def convert_youtube_datetime(yt_datetime_str: str) -> str:
    if not yt_datetime_str or yt_datetime_str == '1970-01-01T00:00:00Z':
        return "1970-01-01 00:00:00"
    clean = yt_datetime_str.replace('Z', '').replace('T', ' ')
    try:
        dt = datetime.fromisoformat(clean)
        return dt.strftime('%Y-%m-%d %H:%M:%S')
    except ValueError:
        return clean[:19] if len(clean) >= 19 else "1970-01-01 00:00:00"

def collect_positive_shorts():
    # Use FEWER, BETTER keywords
    keywords = [
        '"Premnath Ji Maharaj" short',
        '"motivational story" India short',
        '"acts of kindness" India short',
        '"inspirational real story" short'
    ]

    all_shorts = []
    MAX_TO_COLLECT = 20  # Reduce load

    for keyword in keywords:
        if len(all_shorts) >= MAX_TO_COLLECT:
            break
        print(f"🔍 Searching: {keyword}")
        # Fetch only 5 per keyword
        items = fetch_youtube_shorts(keyword, max_results=5)

        for item in items:
            if len(all_shorts) >= MAX_TO_COLLECT:
                break
            video_id = item['id']['videoId']
            details = get_video_details(video_id)
            if not details:
                continue

            status = details.get('status', {})
            if not status.get('embeddable', False):
                print(f"⏭️ Skipping {video_id}: embedding disabled")
                continue

            snippet = details['snippet']
            content_details = details['contentDetails']
            statistics = details.get('statistics', {})

            if not is_valid_short(content_details['duration']):
                continue

            if not is_positive_with_groq(snippet['title'], snippet['description']):
                continue

            short = {
                'video_id': video_id,
                'title': snippet['title'],
                'description': snippet['description'],
                'channel': snippet['channelTitle'],
                'thumbnail': snippet['thumbnails']['high']['url'],
                'published_at': convert_youtube_datetime(snippet['publishedAt']),
                'views': statistics.get('viewCount', '0'),
                'likes': statistics.get('likeCount', '0'),
                'comments': statistics.get('commentCount', '0')
            }

            all_shorts.append(short)
            print(f"✅ Added: {short['title'][:50]}...")

    saved_count = 0
    for short in all_shorts:
        try:
            save_short_to_db(short)
            saved_count += 1
        except Exception as e:
            print(f"⚠️ DB error: {e}")

    print(f"🎉 Total {saved_count} positive shorts saved!")
    return all_shorts