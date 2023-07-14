from rest_framework import viewsets

from .models import Task, Tag, User
from .serializers import UserSerializer, TagSerializer, TaskSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.order_by("id")
    serializer_class = UserSerializer


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.order_by("id")
    serializer_class = TagSerializer
        

class TaskViewSet(viewsets.ModelViewSet):
    queryset = (Task.objects.order_by("id")
                .prefetch_related("tags")
                .select_related("author", "performer")
                )
    serializer_class = TaskSerializer
