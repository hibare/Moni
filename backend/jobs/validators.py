"""Jobs validators"""

from django.core.exceptions import ValidationError
import apprise


def apprise_url_validator(url: str) -> bool:
    """Validate a apprise URL"""

    if url is not None:
        apobj = apprise.Apprise()
        status = apobj.add(url)
        del apobj

        if status:
            return status
        raise ValidationError("Invalid Apprise URL")

    return True
