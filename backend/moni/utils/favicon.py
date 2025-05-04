"""
Find favicon/icon link of a web service
"""

import logging
from typing import Optional, List, Tuple
import bs4
from urllib.parse import urljoin
import requests
from requests.exceptions import RequestException
from django.conf import settings
from moni.requests.urls import get_base_url

logger = logging.getLogger(__name__)


class Favicon:
    """Favicon operations using requests"""

    DEFAULT_FAVICON_PATH = '/favicon.ico'
    ICON_RELS = ['icon', 'shortcut icon', 'apple-touch-icon']
    VALIDATION_TIMEOUT = 10
    FETCH_TIMEOUT = 15
    DEFAULT_HEADERS = {'User-Agent': settings.MONI_USER_AGENT}

    @staticmethod
    def _validate_icon_url(url: str) -> bool:
        """
        Check if URL is live and reachable using HEAD/GET with requests. Content-Type is NOT checked.
        """
        try:
            # Use HEAD request first
            response = requests.head(
                url,
                verify=False,  # Equivalent to verify_ssl=False
                timeout=Favicon.VALIDATION_TIMEOUT,
                allow_redirects=True,  # Allow redirects for HEAD
                headers=Favicon.DEFAULT_HEADERS
            )

            # Check if HEAD request was successful (status code 2xx)
            if response.ok:  # response.ok checks for status_code < 400
                logger.debug("Validated via HEAD: URL=%s, Status=%s", url, response.status_code)
                return True

            # Fallback to GET request if HEAD failed (e.g., 405 Method Not Allowed) or was inconclusive
            logger.debug("HEAD failed or inconclusive for %s (Status: %s), trying GET.", url, response.status_code)
            response = requests.get(
                url,
                verify=False,
                timeout=Favicon.VALIDATION_TIMEOUT,
                headers=Favicon.DEFAULT_HEADERS
            )

            logger.debug("Validating via GET: URL=%s, Status=%s", url, response.status_code)
            return response.ok  # Return True if GET status is 2xx

        except RequestException as e:  # Catch requests-specific exceptions
            logger.warning("Validation network error for URL=%s: %s", url, e)
            return False
        except Exception:
            logger.exception("Unexpected error validating URL=%s", url)
            return False

    @staticmethod
    def get_favicon_url(url: str) -> Optional[str]:
        """Find & return favicon URL using requests"""
        try:
            base_url = get_base_url(url)
            if not base_url:
                logger.warning("Could not determine base URL for: %s", url)
                return None

            # 1. Try default /favicon.ico first
            default_favicon_url = urljoin(base_url, Favicon.DEFAULT_FAVICON_PATH)
            logger.debug("Trying default favicon: %s", default_favicon_url)
            if Favicon._validate_icon_url(default_favicon_url):
                logger.info("Found valid default favicon at: %s", default_favicon_url)
                return default_favicon_url

            # 2. Fetch the page HTML using requests.get
            logger.debug("Fetching page HTML from: %s", base_url)
            response = requests.get(
                base_url,
                verify=False,
                timeout=Favicon.FETCH_TIMEOUT,
                headers=Favicon.DEFAULT_HEADERS
            )

            logger.info("URL=%s, Response Status=%s", base_url, response.status_code)

            # Raise HTTPError for bad responses (4xx or 5xx)
            response.raise_for_status()

            # 3. Parse HTML for <link rel="icon" ...> tags
            page = bs4.BeautifulSoup(response.content, 'html.parser')
            icons: List[Tuple[str, Optional[str]]] = []

            for rel_value in Favicon.ICON_RELS:
                for link_tag in page.find_all('link', attrs={'rel': lambda r: bool(r and rel_value in r.lower())}):
                    # Ensure link_tag is a Tag and has attrs before proceeding
                    if isinstance(link_tag, bs4.Tag) and hasattr(link_tag, 'attrs'):
                        href_val = link_tag.attrs.get('href')
                        # Ensure href is a string (handle potential list values, though unlikely for href)
                        href = str(href_val[0]) if isinstance(href_val, list) else str(href_val)

                        if href:
                            icons.append((href, rel_value))

            logger.debug("Found potential icon links: %s", icons)

            # 4. Resolve and validate found icon URLs
            for href, rel in icons:
                icon_url = urljoin(base_url, href)
                logger.debug("Trying icon link: %s (rel=%s)", icon_url, rel)
                if Favicon._validate_icon_url(icon_url):
                    logger.info("Found valid icon via <link> tag: %s", icon_url)
                    return icon_url

            # 5. If no icon found via <link>, return None
            logger.warning("No valid favicon found via <link> tags for URL: %s", url)
            return None

        except RequestException as e:  # Catch requests-specific exceptions
            logger.error("Request failed during favicon search for URL=%s: %s", url, e)
            return None
        except bs4.FeatureNotFound:
            logger.error("HTML parser not found for BeautifulSoup. Ensure 'html.parser' or 'lxml' is installed.")
            return None
        except Exception:
            logger.exception("Unexpected error processing URL=%s", url)
            return None
