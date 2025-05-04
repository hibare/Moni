"""Helper functions util"""

import re
import uuid
from pathlib import Path
import moni


def get_str_uuid() -> str:
    """Returns UUID as string"""

    return str(uuid.uuid4())


def get_version():
    """
    Return package version as listed in `__version__` in `init.py`.
    """

    return moni.VERSION


def get_title():
    """
    Return app name
    """

    return moni.TITLE


def get_ua() -> str:

    return f"{get_title()}/{get_version()}"
