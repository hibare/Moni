"""
Find favicon/icon link of a web service
"""

import logging
from time import time
import urllib3
import bs4
from urllib.parse import urljoin, urlparse, urlunparse
from moni.utils.urls import get_base_url, parse_url
from moni.utils.requests_proxy import requests_get

logger = logging.getLogger(__name__)


class Favicon:
    """Favicon operations"""

    DEFAULT_FAVICON_PATH = '/favicon.ico'

    @staticmethod
    def get_favicon_url(url: str) -> str:
        """Find & return favicon URL"""

        try:

            base_url = get_base_url(url)
            URLObj = parse_url(url)
            favicon_url = urljoin(base_url, Favicon.DEFAULT_FAVICON_PATH)

            response = requests_get(base_url, verify_ssl=False, timeout=10)

            logger.info("URL=%s, Response=%s", url, response.status)

            if not str(response.status).startswith('2'):
                return None

            page = bs4.BeautifulSoup(response.data, 'html.parser')

            icons = [e for e in page.find_all(
                name='link') if 'icon' in e.attrs.get('rel')]

            if icons:
                favicon_url = icons[0].attrs.get('href')

            parsed = urlparse(favicon_url, scheme='http')

            if not parsed.netloc:
                favicon_url = urlunparse(
                    (parsed.scheme, URLObj.NETLOC, parsed.path, '', '', ''))

            return favicon_url if Favicon.validate_url(favicon_url) else None

        except Exception:
            logger.exception("URL=%s", url)
            return None

    def validate_url(url: str) -> bool:
        """
        Check if URL is live & rechable
        """

        response = requests_get(url, verify_ssl=False, timeout=10)

        return response.status == 200
