import pytest
from unittest.mock import patch
from src.utils import get_content_type
from src.configs import ContentType


@pytest.mark.parametrize(
    "url,expected_type",
    [
        (
            "https://youtu.be/1hWKoPTazMw?feature=shared",
            ContentType.VIDEO,
        ),
        (
            "https://music.youtube.com/watch?v=55TYgbk4kZs&feature=shared",
            ContentType.SONG,
        ),
        (
            "https://www.youtube.com/@FCBarcelona",
            ContentType.CHANNEL,
        ),
        (
            "https://www.youtube.com/watch?v=WUvTyaaNkzM&list=PLZHQObOWTQDMsr9K-rj53DwVRMYO3t5Yr",
            ContentType.PLAYLIST,
        ),
        (
            "https://music.youtube.com/playlist?list=OLAK5uy_ksMcoC36wmr-fyFQfcpM_TjVqo3pBA1H4",
            ContentType.ALBUM,
        ),
    ],
)
def test_get_content_type_with_urls(url, expected_type):
    content_type = get_content_type(url)
    assert content_type == expected_type
