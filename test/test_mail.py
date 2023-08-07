from unittest.mock import patch, MagicMock

from django.core import mail
from django.template.loader import render_to_string
from django.test import override_settings

from main.models import Task
from task_manager.tasks import send_assign_notification
from test.base import TestViewSetBase
from test.fixtures.factories.user import UserFactory
from test.fixtures.factories.task import TaskFactory


@override_settings(CELERY_TASK_ALWAYS_EAGER=True)
class TestSendEmail(TestViewSetBase):
    @patch.object(mail, "send_mail")
    def test_send_assign_notification(self, fake_sender: MagicMock) -> None:
        performer = UserFactory.create()
        task = TaskFactory.create(performer=performer)

        send_assign_notification.delay(task.id)

        fake_sender.assert_called_once_with(
            subject="You've assigned a task.",
            message="",
            from_email=None,
            recipient_list=[performer.email],
            html_message=render_to_string(
                "emails/notification.html",
                context={"task": Task.objects.get(pk=task.id)},
            ),
        )
