from django.urls import path, include
from .views import RegistrationAPIView, LoginAPIView, UserRetrieveUpdateAPIView


urlpatterns = [
    # 회원가입
    path('register/', RegistrationAPIView.as_view()),
    # 로그인
    path('login/', LoginAPIView.as_view()),    
    # 회원정보
    path('update/', UserRetrieveUpdateAPIView.as_view())
]