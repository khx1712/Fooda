from map.models import RestImage, Restaurant, Folder
from rest_framework import serializers
from django.contrib.auth.models import User


class RestImgSerializer(serializers.ModelSerializer):

    class Meta:
        model = RestImage
        fields = ['file_save_name', 'file_origin_name']


class RestaurantSerializer(serializers.ModelSerializer):
    restimages = RestImgSerializer(many=True, read_only=True)

    class Meta:
        model = Restaurant
        fields = ['id', 'name', 'restimages']
    #    fields = ['id', 'name']


class FolderSerializer(serializers.ModelSerializer):
    restaurants = RestaurantSerializer(many=True, read_only=True)

    class Meta:
        model = Folder
        fields = ['id', 'name', 'restaurants']


class UserRestSerializer(serializers.ModelSerializer):
    folders = FolderSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ("id", "username", "folders")


class RestaurantDetailSerializer(serializers.ModelSerializer):
    restimages = RestImgSerializer(many=True, read_only=True)

    class Meta:
        model = Restaurant
        fields = '__all__'

class RestImgDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = RestImage
        fields = '__all__'


class FolderDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Folder
        fields = '__all__'


class CreateFolderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Folder
        fields = '__all__'
