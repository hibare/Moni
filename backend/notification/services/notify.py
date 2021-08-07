"""Send out notifications"""

import logging
from typing import List
from notification.models import Notifications, NotificationsHistory
from notification.services.slack.slack import Slack
from notification.services.discord.discord import Discord
from notification.services.webhook.webhook import Webhook
from notification.services.gotify.gotify import Gotify

logger = logging.getLogger(__name__)


class Notify:
    """Notiy operations"""

    @staticmethod
    def notify(notification_obj: Notifications, title: str, url: str, success: bool, success_status: List, status_code: int, error: str = None):
        if notification_obj.type == 'slack':
            notify = Slack()
            notify.prep_payload(title, url, success,
                                success_status, status_code, error)
            n_status, n_status_code, n_error = notify.send(
                notification_obj.url)

        elif notification_obj.type == 'discord':
            notify = Discord()
            notify.prep_payload(title, url, success,
                                success_status, status_code, error)
            n_status, n_status_code, n_error = notify.send(
                notification_obj.url)

        elif notification_obj.type == 'webhook':
            notify = Webhook()
            notify.prep_payload(title, url, success,
                                success_status, status_code, error)
            n_status, n_status_code, n_error = notify.send(
                notification_obj.url)

        elif notification_obj.type == 'gotify':
            notify = Gotify()
            notify.prep_payload(title, url, success,
                                success_status, status_code, error)
            n_status, n_status_code, n_error = notify.send(
                notification_obj.url)

        else:
            logger.error("Unknown notification uuid=%s, type=%s",
                         notification_obj.uuid, notification_obj.type)
            return

        _ = NotificationsHistory.objects.create(
            uuid=notification_obj,
            status=n_status,
            status_code=n_status_code,
            error=n_error,
        )
