import hashlib
import json
from pathlib import Path
from typing import List

import yt_dlp

from src.configs import (CACHE_DIR, MUSIC, TARGET, ContentType, Formats,
                         format_mappings)


def get_cache_file(url):
    url_hash = hashlib.md5(url.encode()).hexdigest()
    return CACHE_DIR / f"{url_hash}.json"


def save_to_cache(url, data):
    with get_cache_file(url).open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


def load_from_cache(url):
    cache_file = get_cache_file(url)
    if cache_file.exists():
        with cache_file.open("r", encoding="utf-8") as f:
            return json.load(f)
    return None


def get_metadata(url: str) -> dict:
    info = load_from_cache(url)
    if info:
        return info

    ydl_opts = {
        "quiet": True,
        "playlist_items": "1",
        "no_warnings": True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        if info is None:
            raise ValueError("Unable to fetch metadata.")
        while "entries" in info:
            info = info["entries"][0]
        save_to_cache(url, info)
        return info


def get_content_type(url: str) -> ContentType:
    info = get_metadata(url)

    track = info.get("track")
    playlist_id = info.get("playlist_id")
    channel_id = info.get("channel_id")

    if not (track or playlist_id):
        return ContentType.VIDEO
    if track and not playlist_id:
        return ContentType.SONG
    if channel_id == playlist_id:
        return ContentType.CHANNEL
    if track and playlist_id:
        return ContentType.ALBUM

    return ContentType.PLAYLIST


def get_formats(url: str) -> List[Formats]:
    info = get_metadata(url)
    format_ids = {format["format_id"] for format in info["formats"]}
    formats = [
        format
        for format in Formats
        # Check for at least one common format between required and available formats
        if set(format_mappings[format.value]) & format_ids
    ]
    return formats


def download(url: str, format: Formats = Formats.HIGH) -> None:
    info = get_metadata(url)
    filename = "%(title)s.%(ext)s"
    indexed_filename = "%(playlist_index)s - %(title)s.%(ext)s"

    outtmpls = {
        ContentType.VIDEO: f"{TARGET}/{filename}",
        ContentType.SONG: f"{MUSIC}/{filename}",
        ContentType.PLAYLIST: f"{TARGET / info.get('playlist_title', 'Unknown Playlist')}/{indexed_filename}",
        ContentType.ALBUM: f"{MUSIC / info.get('album', 'Unknown Album')}/{indexed_filename}",
        ContentType.CHANNEL: f"{TARGET / info.get('channel', 'Unknown Channel')}/{indexed_filename}",
    }

    video_format = "/".join(format_mappings[format.value])
    audio_format = "/".join(format_mappings["audio"])

    format_code = (
        audio_format
        if get_content_type(url) in [ContentType.SONG, ContentType.ALBUM]
        else f"({video_format})+({audio_format})"
    )

    ydl_opts = {
        "format": format_code,
        "no_warnings": True,
        "writethumbnail": True,
        "writesubtitles": True,
        "subtitleslangs": ["en"],
        "embedsubtitles": True,
        "embedthumbnail": True,
        "postprocessors": [
            {"key": "FFmpegEmbedSubtitle"},
            {"key": "EmbedThumbnail"},
        ],
        "outtmpl": outtmpls[get_content_type(url)],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
