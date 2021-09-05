"""Jobs tests"""

import logging
import pickle
import time
from django.core.exceptions import ValidationError
from django.test import TestCase
from django_apscheduler.models import DjangoJob
from jobs.models import default_success_status, Jobs
from jobs.validators import apprise_url_validator
from jobs import scheduler


logger = logging.getLogger(__name__)


class JobsModelsTests(TestCase):

    def test_default_success_status(self):
        """Test default sucess status"""

        self.assertEqual(default_success_status(), [200])


class JobsTests(TestCase):

    def setUp(self) -> None:
        scheduler.start(default_jobs=False)
        self.obj = Jobs.objects.create(
            url="https://hibare.in",
            title="Hibare.in"
        )

    def tearDown(self) -> None:
        scheduler.shutdown()
        logger.info("Stopping scheduler")
        time.sleep(5)
        return super().tearDown()

    def test_job_operations(self):
        """Test job creation"""
        logger.info("Testing job creation")
        obj = DjangoJob.objects.get(id=self.obj.uuid)
        self.assertEqual(self.obj.uuid, obj.id)

        """Test job active status"""
        logger.info("Testing job active state")
        self.obj.state = True
        self.obj.save()
        obj = DjangoJob.objects.get(id=self.obj.uuid)
        self.assertIsNotNone(pickle.loads(obj.job_state).get('next_run_time'))

        """Test job pause status"""
        logger.info("Testing job pause state")
        self.obj.state = False
        self.obj.save()
        obj = DjangoJob.objects.get(id=self.obj.uuid)
        self.assertIsNone(pickle.loads(obj.job_state).get('next_run_time'))

        """Test job resume status"""
        logger.info("Testing job resume state")
        self.obj.state = True
        self.obj.save()
        obj = DjangoJob.objects.get(id=self.obj.uuid)
        self.assertIsNotNone(pickle.loads(obj.job_state).get('next_run_time'))


class NotificationTests(TestCase):

    def test_notification_url_success(self):
        """Validate a notifier URL (success)"""

        url = "mailto://mySendingUsername:mySendingPassword@example.com?to=receivingAddress@example.com"
        self.assertEqual(apprise_url_validator(url), True)

    def test_notification_url_failure(self):
        """Validate a notifier URL (failure)"""

        url = "mailt://mySendingUsername:mySendingPassword@example.com?to=receivingAddress@example.com"

        with self.assertRaises(ValidationError):
            apprise_url_validator(url)
