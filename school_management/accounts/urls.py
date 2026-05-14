from django.urls import path

from .views import (
    RegisterView,
    MeView,
    LoginView,
    StudentProfileView
)

from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [

    path(
        'register/',
        RegisterView.as_view()
    ),

    path(
        'login/',
        LoginView.as_view()
    ),

    path(
        'token/refresh/',
        TokenRefreshView.as_view()
    ),

    path(
        'me/',
        MeView.as_view()
    ),
    path(
    'student/profile/',
    StudentProfileView.as_view()
    ),
]