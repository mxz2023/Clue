from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.timeimprint import views

router = DefaultRouter()
router.register('timeimprint', views.DateEventViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
