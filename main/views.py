import django_filters

from rest_framework import viewsets, permissions

from typing import cast

from .models import Task, Tag, User
from .serializers import (
    UserSerializer,
    TagSerializer,
    TaskSerializer,
    CountdownJobSerializer,
    )
from .permissions import IsStaffDelete

from django.urls import reverse
from main.services.single_resource import (
    SingleResourceMixin, SingleResourceUpdateMixin
    )

from rest_framework_extensions.mixins import (
    NestedViewSetMixin, CreateModelMixin
    )


class UserFilter(django_filters.FilterSet):
    username = django_filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = User
        fields = ("username",)


class TagFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = Tag
        fields = ("title",)


class TaskFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr="icontains")
    description = django_filters.CharFilter(lookup_expr="icontains")
    status = django_filters.ChoiceFilter(choices=Task.Status.choices)
    tags = django_filters.ModelMultipleChoiceFilter(
        field_name="tags", queryset=Tag.objects.all(), conjoined=True
    )
    author = django_filters.CharFilter(lookup_expr="icontains")
    performer = django_filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = Task
        fields = (
            "title", "description", "status",
            "tags", "author", "performer",
        )


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.order_by("id")
    serializer_class = UserSerializer
    filterset_class = UserFilter
    permision_classes = (IsStaffDelete, permissions.IsAuthenticated)


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.order_by("id")
    serializer_class = TagSerializer
    filterset_class = TagFilter
    permision_classes = (IsStaffDelete, permissions.IsAuthenticated)


class TaskViewSet(viewsets.ModelViewSet):
    queryset = (
        Task.objects.order_by("id")
        .prefetch_related("tags")
        .select_related("author", "performer")
    )
    serializer_class = TaskSerializer
    filterset_class = TaskFilter
    permision_classes = (IsStaffDelete, permissions.IsAuthenticated)


class CurrentUserViewSet(
    SingleResourceMixin, SingleResourceUpdateMixin, viewsets.ModelViewSet
):
    serializer_class = UserSerializer
    queryset = User.objects.order_by("id")

    def get_object(self) -> User:
        return cast(User, self.request.user)


class UserTasksViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    queryset = (
        Task.objects.order_by("id")
        .select_related("author", "performer")
        .prefetch_related("tags")
    )
    serializer_class = TaskSerializer


class TaskTagsViewSet(viewsets.ModelViewSet):
    serializer_class = TagSerializer

    def get_queryset(self):
        task_id = self.kwargs["parent_lookup_task_id"]
        return Task.objects.get(pk=task_id).tags.all()


class CountdownJobViewSet(CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = CountdownJobSerializer

    def get_success_headers(self, data: dict) -> dict[str, str]:
        task_id = data["task_id"]
        return {"Location": reverse("jobs-detail", args=[task_id])}
