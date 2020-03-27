from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from .views import RestaurantDetailAPI, RestaurantAPI, FolderDetailAPI #, FileUploadAPI

urlpatterns = [
    path("restaurants", RestaurantAPI.as_view()),
    path("folder/<int:pk>", FolderDetailAPI.as_view()),
    path("restaurant/<int:pk>", RestaurantDetailAPI.as_view()),
    #path('uploadImg/<int:pk>', FileUploadAPI.as_view(), name="upload")
]
