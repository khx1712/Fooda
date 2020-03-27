from map.models import RestImage, Restaurant, Folder
from rest_framework import serializers
from django.contrib.auth.models import User

class RestImgSerializer(serializers.ModelSerializer):

    class Meta:
        model = RestImage
        fields = ['file_save_name']

class RestaurantSerializer(serializers.ModelSerializer):
    """
    restimages = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='image-url'
    )
    """
    #urls = RestImgSerializer()

    class Meta:
        model = Restaurant
     #   fields = ['id', 'name', 'urls']
        fields = ['id', 'name']

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

    class Meta:
        model = Restaurant
        fields = '__all__'


class FolderDetailSerializer(serializers.ModelSerializer):
    restaurants = RestaurantDetailSerializer(many=True, read_only=True)

    class Meta:
        model = Folder
        fields = ['id', 'name', 'restaurants']
