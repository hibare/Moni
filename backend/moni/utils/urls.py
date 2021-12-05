"""URLs Util"""

import logging
import re
from urllib.parse import urlparse, parse_qs

logger = logging.getLogger(__name__)


class URL:
    SCHEME = NETLOC = HOSTNAME = PORT = PATH = PARAMS = QUERY = FRAGMENTS = USERNAME = PASSWORD = None


def format_url(url: str) -> str:
    """
        Check URL for HTTP(S) schema. Add if its missing.
    """
    DEFAUTL_SCHEME = 'http'

    if not re.match('(?:http|https)://', url):
        return '{}://{}'.format(DEFAUTL_SCHEME, url)
    return url


def get_base_url(url: str) -> str:
    """
    Return base URL for given URL.

    Example:
    Return http://example.com for input http://example.com/path/path

    Return scheme://netloc
    """

    url = format_url(url)
    parsed = parse_url(url)
    return'{uri.SCHEME}://{uri.NETLOC}/'.format(uri=parsed)


def parse_url(url: str) -> dict:
    """Parse a URL into components & return as dict"""

    url_obj = URL()

    try:

        url = format_url(url)

        parsed_url = urlparse(url, 'http')

        url_obj.SCHEME = parsed_url.scheme
        url_obj.NETLOC = parsed_url.netloc
        url_obj.HOSTNAME = parsed_url.hostname
        url_obj.PORT = parsed_url.port
        url_obj.PATH = parsed_url.path
        url_obj.PARAMS = parsed_url.params
        url_obj.QUERY = dict(parse_qs(parsed_url.query))
        url_obj.FRAGMENTS = parsed_url.fragment
        url_obj.USERNAME = parsed_url.username
        url_obj.PASSWORD = parsed_url.password

    except Exception:
        logger.exception("Failed to parse url %s", url)

    return url_obj
