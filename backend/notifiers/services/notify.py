"""Send out notifications"""

import logging
from typing import List
from notifiers.models import Notifiers, NotifiersHistory
from notifiers.services.slack.slack import Slack
from notifiers.services.discord.discord import Discord
from notifiers.services.webhook.webhook import Webhook
from notifiers.services.gotify.gotify import Gotify
from notifiers.services.telegram.telegram import Telegram

logger = logging.getLogger(__name__)


class Notify:
    """Notiy operations"""

    NOTIFIERS = {
        'slack': Slack,
        'discord': Discord,
        'webhook': Webhook,
        'gotify': Gotify,
        'telegram': Telegram
    }

    @staticmethod
    def notify(notification_obj: Notifiers, title: str, url: str, success: bool, success_status: List, status_code: int | None, error: str | None = None):
        """Prepare & send notifier"""

        notifier = Notify.NOTIFIERS.get(notification_obj.type, None)

        if notifier:
            notify = notifier()

        else:
            logger.error("Unknown notifier uuid=%s, type=%s",
                         notification_obj.uuid, notification_obj.type)
            return

        notify.prep_payload(title, url, success,
                            success_status, status_code, error)

        n_status, n_status_code, n_error = notify.send(
            notification_obj.url)

        _ = NotifiersHistory.objects.create(
            uuid=notification_obj,
            status=n_status,
            status_code=n_status_code,
            error=n_error,
        )

    @staticmethod
    def test(notification_obj: Notifiers):
        """Test notifier"""

        n_status = n_status_code = n_error = None

        notifier = Notify.NOTIFIERS.get(notification_obj.type, None)

        if notifier:
            notify = notifier()

        else:
            logger.error("Unknown notifier uuid=%s, type=%s",
                         notification_obj.uuid, notification_obj.type)
            return n_status, n_status_code, n_error

        n_status, n_status_code, n_error = notify.send(
            notification_obj.url)

        return n_status, n_status_code, n_error
