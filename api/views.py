from rest_framework import permissions, generics, views, status
from rest_framework.response import Response
from knox.models import AuthToken
from .serializers import CreateUserSerializer, UserSerializer, LoginUserSerializer
from map.models import Folder
from knox.auth import TokenAuthentication
from django.contrib.auth.models import User
from django.conf import settings


# 회원가입하면 Folder table에 내폴더 자동생성
# Create your views here.
class RegistrationAPI(generics.GenericAPIView):
    serializer_class = CreateUserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid()
        user = serializer.save()
        Folder.objects.create(user=user, name="내폴더")  # 내폴더 생성
        return Response(
            {
               "user": UserSerializer(
                   user, context=self.get_serializer_context()
               ).data,
                "token": AuthToken.objects.create(user)[1],
            }
        )


class LoginAPI(generics.GenericAPIView):
    serializer_class = LoginUserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        return Response(
            {
                "user": UserSerializer(
                    user, context=self.get_serializer_context()
                ).data,
                "token": AuthToken.objects.create(user)[1]
            }
        )


class UserAPI(generics.RetrieveAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = [
        permissions.IsAuthenticated
    ]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user

class CheckidAPI(views.APIView):

    def get(self, request, user_id):
        try:
            User.objects.get(username=user_id)
            return Response({
                "ID is already exist.."
            })
        except User.DoesNotExist:
            return Response({
                "ID is usable!"
            })


