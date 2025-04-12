import re

from aiohttp import web


def is_image_url(url: str) -> bool:
    image_url_pattern = re.compile(r'^https?://.*\.(jpg|jpeg|png|gif|bmp|webp)(\?.*)?$', re.IGNORECASE)
    return bool(image_url_pattern.match(url))


def check_image_url(url: str) -> str:
    if not is_image_url(url):
        raise web.HTTPBadRequest(text='Invalid image URL')
    return url
