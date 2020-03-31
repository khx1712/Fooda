from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from .views import RestaurantDetailAPI, RestaurantAPI, FolderDetailAPI, FileUploadAPI, FileDeleteAPI, FolderAPI
urlpatterns = [
    path("restaurants", RestaurantAPI.as_view()),
    path("folders/<int:folder_id>", FolderAPI.as_view()),
    path("folder/<int:folder_id>", FolderDetailAPI.as_view()),
    path("restaurant/<int:rest_id>", RestaurantDetailAPI.as_view()),
    path('uploadImg', FileUploadAPI.as_view(), name="upload"),
    path("deleteImg/<int:img_id>", FileDeleteAPI.as_view()),
]
