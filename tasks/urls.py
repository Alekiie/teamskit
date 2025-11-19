from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import TaskViewSet, recent_activity

router = DefaultRouter()
router.register(r"tasks", TaskViewSet, basename="tasks")

urlpatterns = [
    path("tasks/recent/", recent_activity, name="recent-activity"),
]

urlpatterns += router.urls
