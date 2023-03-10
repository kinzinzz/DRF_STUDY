
import jwt
from datetime import datetime, timedelta

from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db.models.fields import BooleanField

from .managers import UserManager
from core.models import TimestampedModel


class User(AbstractBaseUser, PermissionsMixin, TimestampedModel):
    
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(db_index=True, unique=True)
    phone_number = models.CharField(max_length=255)
    is_active = BooleanField(default=True)
    is_staff = BooleanField(default=False)
    
    USERNAME_FIELD = 'email'
    
    REQUIRED_FIELDS = [
        'username',
        'phone_number'
    ]
    
    objects = UserManager()
    
    def __str__(self):
        return self.email
    
    def get_full_name(self):
        return self.username
    
    def get_short_name(self):
        return self.username
    
    """
    사용자의 token을 확인할 때 'user.generate_jwt_token( )'으로 확인하기 복잡하기 때문에 보다 간단하게 확인할 수 있도록 'user.token'을 정의. 
    별다른 값 없이 '_generate_jwt_token' 을 통해 return된 값을 반환
    """
    @property
    def token(self):
        return self._generate_jwt_token( )

    # 토큰을 발행하는 함수입니다
    def _generate_jwt_token(self):
        dt = datetime.now( ) + timedelta(days=60)

        token = jwt.encode({
            'id': self.pk,
            'exp': dt.utcfromtimestamp(dt.timestamp())
        }, settings.SECRET_KEY, algorithm='HS256')

        return token