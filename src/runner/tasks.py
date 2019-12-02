import celery
from monitor.celery import app
from decouple import config
from runner.models import Monitors
import traceback
from celery.utils.log import get_task_logger
import requests
import json
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
import os.path

logger = get_task_logger(__name__)


class BaseTask(celery.Task):
    def on_failure(self, exc, task_id, args, kwargs, einfo):
        messageRecipient = config('ADMIN_RECIPIENT')
        body = "<strong>Celery Worker Failed</strong><br/><br/>"\
            "<strong>Task id: </strong> {}<br/><br/>"\
            "<strong>Exc: </strong> {}<br/><br/>"\
            "<strong>Args: </strong> {}<br/><br/>"\
            "<strong>Kwargs: </strong> {}<br/><br/>"\
            "<strong>Einfo: </strong> {}<br/><br/>".format(
                task_id, exc, args, kwargs, einfo)

        logger.error("Task failed: %s", einfo)

        sendMail(subject="[Crazy Wizard] Celery task failed",
                 recipient=messageRecipient, htmlBody=body)


@app.task(base=BaseTask, name="Task runner")
def task_runner():
    check_urls = retrieve_entries()
    for url_dict in check_urls:
        run_health_check.delay(url_dict)


def retrieve_entries():
    # Local vars
    check_urls = list()

    # Get all active monitor entries from DB
    logger.info("Retrieving active monitors")
    monitors = Monitors.objects.all().filter(active=True)
    if monitors:
        for monitor in monitors:
            monitor_dict = dict()
            check_url = monitor.health_check_url
            logger.info("Found health check URL=%s", check_url)
            monitor_dict.update(
                dict(
                    url=monitor.health_check_url,
                    mail_recipient=monitor.mail_recipient,
                    slack_endpoint=monitor.slack_endpoint
                )
            )
            check_urls.append(monitor_dict)
    else:
        logger.info("No active monitors found")

    return check_urls


@app.task(base=BaseTask, name="Run health checks", bind=True)
def run_health_check(self, data):
    # Local vars
    failure_status_codes = ('5')
    url = data.get('url')
    mail_recipient = data.get('mail_recipient')
    slack_endpoint = data.get('slack_endpoint')

    try:
        logger.info("Running health check on URL=%s", url)
        response = requests.get(url)
        logger.info("Received status=%s for URL=%s, response=%s",
                    response.status_code, url, response.content)

        # Check for status code to determine status of health check
        if str(response.status_code).startswith(failure_status_codes):
            logger.warning("Health check failed, URL=%s, status=%s",
                           url, response.status_code)

            # send mail and slack notification
            send_health_check_notification_mail.delay(
                mail_recipient, url, response.status_code)
            send_health_check_notification_slack.delay(
                slack_endpoint, url, response.status_code)
    except Exception as e:
        logger.error("Exception: %s", traceback.format_exc())
        logger.info("Retrying task")
        self.retry(exc=e, countdown=10, max_retries=2)


@app.task(base=BaseTask, name="Send health check notification [Mail]")
def send_health_check_notification_mail(recipient, url, status):
    if recipient:
        body = "<strong> Website down </strong><br/><br/>"\
            "<strong>Status:</strong> %s<br/>"\
            "<strong>URL:<strong> %s<br/>" % (status, url)

        sendMail(subject="[Crazy Wizard] Website down",
                 recipient=recipient, htmlBody=body)


@app.task(base=BaseTask, name="Send health check notification [Slack]")
def send_health_check_notification_slack(endpoint, url, status):
    if endpoint:
        headers = {
            'Content-type': 'application/json',
        }

        text = "Health check failed.\n\nStatus: %s\nURL: %s" % (status, url)

        data = dict(
            text=text,
        )

        try:
            response = requests.post(
                endpoint, headers=headers, data=json.dumps(data))
            logger.info("Slack notification sent, slack status=%s, response=%s",
                        response.status_code, response.content)
        except Exception as e:
            logger.error("Exception: url=%s, status=%s, error=%s",
                         url, status, traceback.format_exc())


def sendMail(subject, recipient, plainBody=None, htmlBody=None, attachment=None):

    try:
        # Create message
        subject = "" + subject
        msg = EmailMultiAlternatives(
            subject, plainBody, settings.DEFAULT_FROM_EMAIL, [recipient])

        if htmlBody is not None:
            msg.attach_alternative(htmlBody, 'text/html')

        if attachment is not None:
            filename = attachment
            if os.path.exists(filename) and os.path.isfile(filename):
                msg.attach_file(filename)

        msg.send()

        logger.info("Mail sent, recipient=%s", recipient)

    except Exception as error:
        logger.error("Exception in mailer. Error=%s", traceback.format_exc())
