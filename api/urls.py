from django.urls import path, include
from .views import RegistrationAPI, LoginAPI, UserAPI, CheckidAPI
from knox import views as knox_views


urlpatterns = [
    path("auth/register", RegistrationAPI.as_view()),
    path("auth/login", LoginAPI.as_view()),
    path("auth/user", UserAPI.as_view()),
    path("auth/logout", knox_views.LogoutView.as_view(), name='knox_logout'),
    path("checkid/<user_id>", CheckidAPI.as_view()),
    path("map/", include("map.urls")),
]