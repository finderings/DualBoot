from django.urls import (
    path,
    include,
    re_path,
)

from main import views
from main.admin import task_manager_admin_site
from main.services.single_resource import BulkRouter

from rest_framework import permissions
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
    openapi.Info(
        title="Snippets API",
        default_version="v1",
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


router = BulkRouter()
router.register(r"users", views.UserViewSet, basename="users")
router.register(r"tasks", views.TaskViewSet, basename="tasks")
router.register(r"tags", views.TagViewSet, basename="tags")
router.register(
    r"current-user", views.CurrentUserViewSet, basename="current_user"
    )
router.register(r"countdown", views.CountdownJobViewSet, basename="countdown")
router.register(r"jobs", views.AsyncJobViewSet, basename="jobs")

users = router.register(r"users", views.UserViewSet, basename="users")
users.register(
    r"tasks",
    views.UserTasksViewSet,
    basename="user_tasks",
    parents_query_lookups=["performer_id"],
)

tasks = router.register(r"tasks", views.TaskViewSet, basename="tasks")
tasks.register(
    r"tags",
    views.TaskTagsViewSet,
    basename="task_tags",
    parents_query_lookups=["task_id"],
)

urlpatterns = [
    path("admin/", task_manager_admin_site.urls),
    path("api/", include(router.urls)),
    re_path(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    re_path(
        r"^swagger/$",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    re_path(
        r"^redoc/$",
        schema_view.with_ui("redoc", cache_timeout=0),
        name="schema-redoc"
    ),
    path('api/token/',
         TokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('api/token/refresh/',
         TokenRefreshView.as_view(),
         name='token_refresh'),
]
