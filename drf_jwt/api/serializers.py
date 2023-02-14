from rest_framework import serializers
from django.contrib.auth import authenticate
from django.utils import timezone
from .models import User

'''
ModelSerializer에서는 create method와 update method를 사용할 수 있다. 
update method는 따로 정의하지 않았는데, 이런 경우 DRF에서 제공하는 기본 update method를 사용한ㄷ.
'''

class RegistrationSerializer(serializers.ModelSerializer):
    '''
    password 필드에 write_only 옵션을 넣어준 이유는 password를 
    updating, creating 할 때는 사용되지만, serializing 할 때는 포함되지 않도록 하기 위해
    '''
    password = serializers.CharField(
        max_length = 128,
        min_length = 8,
        write_only = True
    )
    
    token = serializers.CharField(max_length=255, read_only=True)
    
    class Meta:
        model = User
        fields = [
            'email', 
            'username',
            'phone_number',
            'password',
            'token'
            ]
        
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

# 로그인
class LoginSerializer(serializers.Serializer):
  
    email = serializers.EmailField()
    username = serializers.CharField(max_length=255, read_only=True)
    password = serializers.CharField(max_length=128, write_only=True) # 입력받지만 반환값으로 출력하지 않음
    last_login = serializers.CharField(max_length=255, read_only=True)
        
    def validate(self, data):
        email = data.get('email', None)
        password = data.get('password', None)
        
        if email is None:
            raise serializers.ValidationError(
                'An email address is required to log in.'
            )
        
        if password is None:
            raise serializers.ValidationError(
                'A password is required to log in.'
            )
        # authenticate' method는 email과 password를 받아 그 조합을 데이터베이스에 있는 email과 password 조합을 매칭
        user = authenticate(username=email, password=password)
               
        if user is None:
            raise serializers.ValidationError(
                'A user with this email and password was not found'
            )
        
        if not user.is_active:
            raise serializers.ValidationError(
                'This user has been deactivated.'
            )
             
        user.last_login = timezone.now()
        user.save(update_fields=['last_login'])
        
        return {
            'email': user.email,
            'username': user.username,
            'last_login': user.last_login
        }    

# 회원정보
class UserSerializer(serializers.ModelSerializer):
    
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )
    
    class Meta:
        model = User
        fields = [
            'email',
            'username',
            'password',
            'token'
        ]
        
        # 회원가입할 때는 password입력 시 property: 속성값를 지정해야 하지만
        # token field에 대해서는 그럴 이유가 없기 때문에 'read_only_fields'로 따로 작성
        read_only_fields = ('token', )
        
    
    def update(self, instance, validated_data):
        
        password = validated_data.pop('password', None)
        
        for (key, value) in validated_data.items():
            
            setattr(instance, key, value)

        if password is not None:
            # Django에서 비밀번호는 처리하는 함수를 따로 제공한다. 
            instance.set_password(password)
        
        instance.save()

        return instance