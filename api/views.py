from rest_framework import permissions, generics, status
from rest_framework.response import Response
from knox.models import AuthToken
from .serializers import CreateUserSerializer, UserSerializer, LoginUserSerializer
from knox.auth import TokenAuthentication
from django.conf import settings

"""
def mkdir(user_id):
    import os
    import errno

    dir_path = os.path.join(settings.MEDIA_ROOT, user_id)
    
    try:
        if not (os.path.isdir(dir_path)):
            os.makedirs(os.path.join(dir_path, 'restaurant'))
            os.makedirs(os.path.join(dir_path, 'dirary'))
            return True
    except OSError as e:
        if e.errno != errno.EEXIST:
            return False
"""

# 회원가입하면 내폴더 자동생성

# Create your views here.
class RegistrationAPI(generics.GenericAPIView):
    serializer_class = CreateUserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        # mkdir(user.id)
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


