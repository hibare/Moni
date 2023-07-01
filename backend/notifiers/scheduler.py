"""Schedule notifier jobs"""

from django.conf import settings
from notifiers.models import NotifiersHistory


def delete_old_notifier_history():
    """This job delete all notifier history older than `settings.NOTIFIER_HISTORY_PURGE_AGE` (in days) from the database"""

    NotifiersHistory.objects.delete_old_history(
        settings.NOTIFIER_HISTORY_PURGE_AGE)
