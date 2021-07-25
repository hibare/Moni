"""Helper functions util"""

import re
import uuid
from pathlib import Path


def get_str_uuid() -> str:
    """Returns UUID as string"""

    return str(uuid.uuid4())


def get_version(package: str = 'moni'):
    """
    Return package version as listed in `__version__` in `init.py`.
    """
    init_py = open(Path(package, '__init__.py')).read()
    return re.match("__version__ = ['\"]([^'\"]+)['\"]", init_py).group(1)
