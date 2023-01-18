from rest_framework import serializers
from .models import User
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed
from .utils import Util
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=30, min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'mobile', 'password')

    def validate(self, attrs):
        email = attrs.get('email', '')
        mobile = str(attrs.get('mobile', ''))

        if not mobile.isdigit():
            raise serializers.ValidationError(
                'Mobile number should be numeric'
            )
        return attrs
    
    def create(self, validated_data):
        user = super(UserSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user
    
class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=255)

    class Meta:
        model = User
        fields = {'token'}

class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=12)
    password = serializers.CharField(max_length=30, min_length=8, write_only=True)
    first_name = serializers.CharField(max_length=30, read_only=True)
    last_name = serializers.CharField(max_length=30, read_only=True)

    class Meta:
        model = User
        fields = ('email', 'password', 'first_name', 'last_name', 'tokens')
        
    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', '')

        user = auth.authenticate(email=email, password=password)

        if not user:
            raise AuthenticationFailed('Invalid credentials')
        if not user.is_active:
            raise AuthenticationFailed('Esta cuenta no esta activa, porfavor verifica tu cuenta o contacta con el soporte')
        if not user.is_verified:
            raise AuthenticationFailed('Esta cuenta no esta verificada, porfavor verifica tu cuenta o contacta con el soporte')
        
        return{
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'tokens': user.tokens(),
        }

        return super().validate(attrs)

class ResetPasswordSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=12)

    class Meta:
        fields = ['email']

class SetNewPasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=30, min_length=8, write_only=True)
    token = serializers.CharField(min_length=6, write_only=True)
    uidb64 = serializers.CharField(min_length=2, write_only=True)

    class Meta:
        model = User
        fields = ['password', 'token', 'uidb64']
        
    def validate(self, attrs):
        try:
            password = attrs.get('password')
            token = attrs.get('token')
            uidb64 = attrs.get('uidb64')
            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed('El link es invalido', 401)
            user.set_password(password)
            user.save()

            return (user)
        except Exception as e:
            raise AuthenticationFailed('El link es invalido', 401)