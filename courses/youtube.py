import re

_PATTERNS = [
    re.compile(r'(?:v=|/embed/|youtu\.be/)([A-Za-z0-9_-]{11})'),
]


def extract_video_id(url):
    """Pulls the 11-character YouTube video ID out of any common URL shape
    (watch?v=, youtu.be/, /embed/). Returns None if nothing matches."""
    if not url:
        return None
    for pattern in _PATTERNS:
        match = pattern.search(url)
        if match:
            return match.group(1)
    return None


def build_embed_url(url):
    """Turns a stored YouTube URL into a nocookie embed URL, or None."""
    video_id = extract_video_id(url)
    if not video_id:
        return None
    return f'https://www.youtube-nocookie.com/embed/{video_id}?rel=0&modestbranding=1'
