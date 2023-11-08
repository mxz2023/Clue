from django.urls import path, include

from apps.mxz_userinfo import views


urlpatterns = [
    path('reg', views.user_reg),
    path('login', views.user_login),
    path('logout', views.user_logout),
    path('modify', views.user_modify),
]
