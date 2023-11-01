from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.mxz_timeimprint import views

router = DefaultRouter()
router.register('timeimprint', views.MxzDateEventViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
