import os
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import Http404
from .serializers import RestaurantSerializer, RestImgDetailSerializer, FolderDetailSerializer, UserRestSerializer, RestaurantDetailSerializer, FolderSerializer
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


class FolderAPI(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = [
        permissions.IsAuthenticated
    ]

    def get(self, request, pk):
        folders = Folder.objects.get(id=pk)
        serializer = FolderSerializer(folders)
        return Response(serializer.data)


#
class FolderDetailAPI(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = [
        permissions.IsAuthenticated
    ]

    def get_object(self, folder_id):
        try:
            return Folder.objects.get(id=folder_id)
        except Folder.DoesNotExist:
            raise Http404

    def get(self, request, folder_id):
        folders = self.get_object(folder_id)
        serializer = FolderDetailSerializer(folders)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = RestaurantSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, folder_id, format=None):
        folders = self.get_object(folder_id)
        serializer = FolderDetailSerializer(folders, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # rest_id 를 pk로 보내줘야함
    def delete(self, request, folder_id, format=None):
        folder = self.get_object(folder_id)
        folder.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class RestaurantDetailAPI(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = [
        permissions.IsAuthenticated
    ]

    # 조건에 해당하는 인스턴스가 있는지 찾아주고 있으면 리턴해준다.
    def get_object(self, rest_id):
        try:
            return Restaurant.objects.get(id=rest_id)
        except Restaurant.DoesNotExist:
            raise Http404

    #  user_id 를 pk로 보내줘야함
    def get(self, request, rest_id, format=None):
        restaurant = self.get_object(rest_id)
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
    def put(self, request, rest_id, format=None):
        restaurant = self.get_object(rest_id)
        serializer = RestaurantDetailSerializer(restaurant, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # rest_id 를 pk로 보내줘야함
    def delete(self, request, rest_id, format=None):
        restaurant = self.get_object(rest_id)
        restaurant.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


 # POST로 이미지를 받을때 data에 실어서 받아야 하나 아니면 url로 받아야 하나 그에 따른 argument의 차이가 무엇인가 (pk <-> argv, kwargs)
 # 이미지를 받으면 Restaurant instance에서 이미지와 매칭되는 것을 추가해줘야 한다.
 # delete를 구현해야한다 / Restaurant instance에서 이미지와 매칭되는 것을 추가해줘야 한다.
class FileUploadAPI(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = [
        permissions.IsAuthenticated
    ]

    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
    
        # multipart로 데이터를 보내면 변환 시켜줘야 한다 기본적으로 json 으로 보내는 것은 dict 형식이다 
        # 요청된 데이터를 꺼냄( QueryDict) <QueryDict: {'file_name': [<InMemoryUploadedFile: 돈까스.jpeg" (image/jpeg)>]}>
        new_data = request.data.dict()

        # 요청된 파일 객체
        # {'file_name': <InMemoryUploadedFile: 돈까스.jpeg" (image/jpeg)>}, 이름에 " 이 붙어 이걸 처리해줘야됨
        # file_name.name[:-1] => 돈까스.jpeg
        if request.data['file_name'].name[-1] == '"':
            request.data['file_name'].name = request.data['file_name'].name[:-1]
        file_name = request.data['file_name']

        # 저장될 파일의 path를 생성
        # C:\Users\user\PycharmProjects\FooDa\image\2020\03\29\0654b9082d804fd3a8be6aaa04d0dc17_20200329123242.jpeg
        new_file_full_name = file_upload_path(file_name.name)

        # 새롭게 생성된 파일의 경로
        # new_file_full_name.split('\\') => ['C:', 'Users', 'user', 'PycharmProjects', 'FooDa', .... , 'filename.jpeg']
        file_path = '\\'.join(new_file_full_name.split('\\')[0:-1])  # (\\)으로 연결하여 파일 이름을 제거한 경로 생성
        # file_path => C:\Users\user\PycharmProjects\FooDa\image\2020\03\29

        # 파일 확장자
        # os.path.splitext(file_name.name) => ('돈까스', '.jpeg')
        file_ext = os.path.splitext(file_name.name)[1]

        # QueryDict에 새로운 데이터 추가( DB와 매핑을 위해서)
        new_data['restaurant'] = request.data['restaurant']
        new_data['file_ext'] = file_ext
        new_data['file_path'] = file_path
        new_data['file_origin_name'] = request.data['file_name'].name
        new_data['file_save_name'] = request.data['file_name']

        new_query_dict = QueryDict('', mutable=True)
        new_query_dict.update(new_data)

        image_serializer = RestImgDetailSerializer(data=new_query_dict)
        if image_serializer.is_valid():
            image_serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(image_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FileDeleteAPI(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = [
        permissions.IsAuthenticated
    ]

    def get_object(self, img_id):
        try:
            return RestImage.objects.get(id=img_id)
        except RestImage.DoesNotExist:
            raise Http404

    def delete(self, request, img_id, format=None):
        image = self.get_object(img_id)
        path = str(image.file_save_name)
        image.delete()
        if os.path.isfile(path):
            os.remove(path)
        return Response(status=status.HTTP_204_NO_CONTENT)
