import argparse

from src.configs import Formats
from src.utils import download


def main():
    parser = argparse.ArgumentParser(description="Download YouTube videos")
    parser.add_argument("url", help="URL of the YouTube video to download")
    parser.add_argument(
        "--quality",
        "-q",
        choices=["high", "medium", "low"],
        default="high",
        help="Video quality (high/medium/low)",
    )

    args = parser.parse_args()

    url = args.url
    quality_input = args.quality

    if quality_input == "high":
        quality = Formats.HIGH
    elif quality_input == "medium":
        quality = Formats.MEDIUM
    elif quality_input == "low":
        quality = Formats.LOW
    else:
        quality = Formats.HIGH  # Default fallback

    download(url, quality)


if __name__ == "__main__":
    main()
