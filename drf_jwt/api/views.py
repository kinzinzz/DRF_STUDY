from rest_framework import status

'''
permission_classes 속성은 누가 이 view를 사용할 수 있는지에 대한 범위를 결정합니다. 
보안을 위해서 로그인 한 유저, 권한이 있는 유저만 접근하도록 할 수 있습니다. 
'''

from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateAPIView

from .serializers import RegistrationSerializer, LoginSerializer, UserSerializer
from .renders import UserJSONRenderer

# 회원가입
class RegistrationAPIView(APIView):
    permission_classes = (AllowAny,) # 사용자 등록(회원가입)은 누구나 가능
    serializer_class = RegistrationSerializer # serializer_class 는 앞서 만들었던 serializer를 지정
    renderer_classes = (UserJSONRenderer,)
    
    def post(self, request):
        user = request.data
        
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

# 로그인
class LoginAPIView(APIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = LoginSerializer
        
    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
       
        return Response(serializer.data, status=status.HTTP_200_OK)

# 회원정보
class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = UserSerializer
    
    def get(self, request, *args, **kwargs):
        
        serializer = self.serializer_class(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def patch(self, request, *args, **kwargs):
        serializer_data = request.data
        
        serializer = self.serializer_class(
            request.user, data=serializer_data, partial=True
        )# partial은 부분 업데이트가 가능하도록 하는 옵션
        
        serializer.is_valid(raise_exception=True)
        
        serializer.save()
        
        return Response(serializer.data, status=status.HTTP_200_OK)