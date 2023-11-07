from django.urls import path, include

from apps.mxz_userinfo import views


urlpatterns = [
    path('reg', views.user_reg),
]
