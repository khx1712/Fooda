from django.urls import path
from .views import RegistrationAPI

urlpatterns = [
    path("auth/register/", RegistrationAPI.as_view()),
]