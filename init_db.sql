CREATE TABLE IF NOT EXISTS youtube_shorts (
    video_id VARCHAR(50) PRIMARY KEY,
    title TEXT,
    description TEXT,
    thumbnail TEXT,
    channel TEXT,
    published_at TIMESTAMP,
    views BIGINT,
    likes BIGINT,
    comments BIGINT
);