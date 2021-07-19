"""urllib3 request proxy"""

import ssl
import time
import logging
from typing import Dict
import urllib3

logger = logging.getLogger(__name__)


def requests_get(url: str, headers: Dict = dict, timeout: int = 20, verify_ssl: bool = True, check_redirect: bool = True):
    """urllib3 GET request proxy"""

    if verify_ssl:
        cert_reqs = ssl.CERT_REQUIRED
    else:
        cert_reqs = ssl.CERT_NONE

    http = urllib3.PoolManager(cert_reqs=cert_reqs)

    start = time.time()
    response = http.request(
        'GET',
        url,
        headers=headers,
        timeout=timeout,
        redirect=check_redirect
    )
    end = time.time()
    elapsed_seconds = end - start

    logger.debug("Request- method=GET, url=%s, round_trip_time=%s",
                 url, elapsed_seconds)

    return response


def requests_post(url: str, body: str, headers: Dict, timeout: int = 20, verify_ssl: bool = True, check_redirect: bool = True):
    """urllib3 GET request proxy"""

    if verify_ssl:
        cert_reqs = ssl.CERT_REQUIRED
    else:
        cert_reqs = ssl.CERT_NONE

    http = urllib3.PoolManager(cert_reqs=cert_reqs)

    start = time.time()
    response = http.request(
        'POST',
        url,
        headers=headers,
        timeout=timeout,
        body=body,
        redirect=check_redirect
    )
    end = time.time()
    elapsed_seconds = end - start

    logger.debug("Request: method=GET, url=%s, round_trip_time=%s",
                 url, elapsed_seconds)

    return response
