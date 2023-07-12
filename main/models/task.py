from django.db import models
from .user import User
from .tag import Tag


class Task(models.Model):
    class Status(models.TextChoices):
        NEW_TASK = "new_task"
        IN_DEVELOMENT = "in_development"
        ARCHIVED = "archived"
        IN_QA = "in_qa"
        IN_CODE_REvIEW = "in_code_review"
        READY_FOR_RELEASE = "ready_fore_release"
        RELEASED = "released"

    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    date_created = models.DateTimeField(auto_now_add=True)
    date_changed = models.DateTimeField(auto_now=True)
    final_date = models.DateTimeField(blank=True, null=True)
    status = models.CharField(
        max_length=255, default=Status.NEW_TASK, choices=Status.choices
    )
    priority = models.CharField(max_length=255)
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="author")
    performer = models.ForeignKey(
        User, on_delete=models.DO_NOTHING, related_name="performer"
    )
    tags = models.ManyToManyField(Tag)
