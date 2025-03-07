from src.configs import Formats
from src.utils import download, get_content_type

if __name__ == "__main__":
    video_url = "https://youtu.be/WUvTyaaNkzM?feature=shared"
    download(video_url)
