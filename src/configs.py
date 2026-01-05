import os
from enum import Enum
from pathlib import Path

from platformdirs import user_cache_dir

ON_ANDROID = "ANDROID_STORAGE" in os.environ
HOME = Path("/sdcard") if ON_ANDROID else Path.home()
TARGET = HOME / "YouTube Videos"
MUSIC = HOME / "Music"
CACHE_DIR = Path(user_cache_dir("ytd-go"))
CACHE_DIR.mkdir(parents=True, exist_ok=True)


class ContentType(Enum):
    ALBUM = "album"
    CHANNEL = "channel"
    PLAYLIST = "playlist"
    SONG = "song"
    VIDEO = "video"


class Formats(Enum):
    HIGH = "1080p"
    MEDIUM = "720p"
    LOW = "480p"


format_mappings = {
    "1080p": ["137", "248", "bestvideo"],
    "720p": ["136", "247", "bestvideo"],
    "480p": ["135", "244", "bestvideo"],
    "audio": ["bestaudio[ext=m4a]", "bestaudio"],
}
