import os
from rest_framework import permissions, generics, status
from rest_framework.response import Response
from rest_framework.parsers import FileUploadParser
from rest_framework.views import APIView
from django.http import Http404
from knox.models import AuthToken
from .serializers import RestaurantSerializer, RestImgSerializer, FolderDetailSerializer, UserRestSerializer, RestaurantDetailSerializer
from .models import Restaurant, RestImage, Folder
from knox.auth import TokenAuthentication
from django.contrib.auth.models import User
from rest_framework.parsers import MultiPartParser, FormParser
from map import file_upload_path
from django.http.request import QueryDict



class RestaurantAPI(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = [
        permissions.IsAuthenticated
    ]

    def get(self, request, *args, **kwargs):
        restaurant = User.objects.get(id=request.user.id)
        serializer = UserRestSerializer(restaurant)
        return Response(serializer.data)

#
class FolderDetailAPI(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = [
        permissions.IsAuthenticated
    ]

    def get(self, request, pk):
        folders = Folder.objects.get(id=pk)
        serializer = FolderDetailSerializer(folders)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = RestaurantDetailSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class RestaurantDetailAPI(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = [
        permissions.IsAuthenticated
    ]

    # 조건에 해당하는 인스턴스가 있는지 찾아주고 있으면 리턴해준다.
    def get_object(self, pk):
        try:
            return Restaurant.objects.get(id=pk)
        except Restaurant.DoesNotExist:
            raise Http404

    #  user_id 를 pk로 보내줘야함
    def get(self, request, pk, format=None):
        restaurant = self.get_object(pk)
        serializer = RestaurantDetailSerializer(restaurant)
        return Response(serializer.data)

    # 상관없음
    def post(self, request, *args, **kwargs):
        serializer = RestaurantDetailSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # rest_id 를 pk로 보내줘야함
    def put(self, request, pk, format=None):
        restaurant = self.get_object(pk)
        serializer = RestaurantDetailSerializer(restaurant, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # rest_id 를 pk로 보내줘야함
    def delete(self, request, pk, format=None):
        restaurant = self.get_object(pk)
        restaurant.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

'''
 # POST로 이미지를 받을때 data에 실어서 받아야 하나 아니면 url로 받아야 하나 그에 따른 argument의 차이가 무엇인가 (pk <-> argv, kwargs)
 # 이미지를 받으면 Restaurant instance에서 이미지와 매칭되는 것을 추가해줘야 한다.
 # delete를 구현해야한다 / Restaurant instance에서 이미지와 매칭되는 것을 추가해줘야 한다.
class FileUploadAPI(APIView):
    """
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    """
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):

        # 요청된 데이터를 꺼냄( QueryDict)
        new_data = request.data.dict()

        # 요청된 파일 객체
        file_name = request.data['file_name']

        # 저장될 파일의 path를 생성
        new_file_full_name = file_upload_path(file_name.name)

        # 새롭게 생성된 파일의 경로
        file_path = '\\'.join(new_file_full_name.split('\\')[0:-1])

        # 파일 확장자
        file_ext = os.path.splitext(file_name.name)[1]

        # QueryDict에 새로운 데이터 추가( DB와 매핑을 위해서)
        new_data['restaurant'] = request.data['restaurant']
        new_data['file_ext'] = file_ext
        new_data['file_path'] = file_path
        new_data['file_origin_name'] = request.data['file_name'].name
        new_data['file_save_name'] = request.data['file_name']

        new_query_dict = QueryDict('', mutable=True)
        new_query_dict.update(new_data)

        image_serializer = RestImgSerializer(data=new_query_dict)
        if image_serializer.is_valid():
            image_serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(image_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    #def delete(self, request, pk, format=None):
'''
