from rest_framework import serializers
from typing import Any

from .models import User, Tag, Task
from task_manager import settings
from task_manager.tasks import countdown

from django.core.files.base import File
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from celery.result import AsyncResult


class FileMaxSizeValidator:
    def __init__(self, max_size: int) -> None:
        self.max_size = max_size

    def __call__(self, value: File) -> None:
        if value.size > self.max_size:
            raise ValidationError(f"Maximum size {self.max_size} exceeded.")


class UserSerializer(serializers.ModelSerializer):
    avatar_picture = serializers.FileField(
        required=False,
        validators=[
            FileMaxSizeValidator(settings.UPLOAD_MAX_SIZES["avatar_picture"]),
            FileExtensionValidator(["jpeg", "jpg", "png"]),
        ],
    )

    class Meta:
        model = User
        fields = (
            'id', 'username', 'first_name', 'last_name',
            'email', 'date_of_birth', 'phone', "avatar_picture", 'role',
        )
            

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'title')


class TaskSerializer(serializers.ModelSerializer):
    author = UserSerializer(required=False)
    performer = UserSerializer(required=False)
    tags = TagSerializer(many=True, required=False)
    
    class Meta:
        model = Task
        fields = (
            'id', 'title', 'description', 'date_created',
            'date_changed', 'final_date', 'status',
            'priority', 'author', 'performer', 'tags'
        )


class RepresentationSerializer(serializers.Serializer):
    def update(self, instance: Any, validated_data: dict) -> Any:
        pass

    def create(self, validated_data: dict) -> Any:
        pass


class CountdownJobSerializer(RepresentationSerializer):
    seconds = serializers.IntegerField(write_only=True)

    task_id = serializers.CharField(read_only=True)
    status = serializers.CharField(read_only=True)

    def create(self, validated_data: dict) -> AsyncResult:
        return countdown.delay(**validated_data)
