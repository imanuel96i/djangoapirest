from django.shortcuts import render
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from rest_framework import generics, status, views
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from .serializers import EmailVerificationSerializer, LoginSerializer, ResetPasswordSerializer, UserSerializer, SetNewPasswordSerializer
from .utils import Util
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
import jwt
from django.conf import settings

class UserCreateAPIView(generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data

        user = User.objects.get(email=user_data['email'])

        token = RefreshToken.for_user(user).access_token

        current_site = get_current_site(request).domain
        relativeLink = reverse('verify')
        absurl = current_site+relativeLink+'?token='+str(token)
        email_body = 'Hola ' + user.first_name + ' ' + user.last_name + '\n\n' + 'Para verificar tu cuenta, haz click en el siguiente enlace: \n' + absurl
        data={'email_body':email_body,
            'to_email':user.email,
            'email_subject':'Verificación de cuenta'}
        Util.send_email(data)

        return Response(user_data, status=status.HTTP_201_CREATED)

    @classmethod
    def get_extra_actions(cls):
        return []
class VerifyEmail(generics.GenericAPIView):

    def get(self, request):
        token = request.GET.get('token')
        print(token)
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user = User.objects.get(id=payload['user_id'])
            if user.is_verified:
                return Response({'email':'Esta cuenta ya esta verificada'}, status=status.HTTP_200_OK)
            if not user.is_verified:
                user.is_verified = True
                user.is_active = True
                user.save()
                return Response({'email': 'Se ha activado correctamente el usuario'}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError as indetifier:
            return Response({'error': 'Ha expirado el tiempo para activar la cuenta'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as indetifier:
            return Response({'error': 'Token invalido'}, status=status.HTTP_400_BAD_REQUEST)
        
class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

class RequestPasswordReset(generics.GenericAPIView):
    serializer_class = ResetPasswordSerializer
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        email = request.data['email']
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            current_site = get_current_site(request=request).domain
            relativeLink = reverse(
                'reset-password-confirm', kwargs={'uidb64': uidb64, 'token': token})
            absurl = 'http://' + current_site + relativeLink
            email_body = 'Hola! \n Haz click en el siguiente link para reiniciar tu contraseña \n' + absurl
            data={'email_body':email_body,
                'to_email':user.email,
                'email_subject':'Reinicio de contraseña'}
            Util.send_email(data)

        return Response({'success':'Se ha enviado un correo para restablecer la contraseña'}, status=status.HTTP_200_OK)

class PasswordTokenCheckAPI(generics.GenericAPIView):
    def get(self, request, uidb64, token):
        
        try:
            id=smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({'error':'Token invalido'}, status=status.HTTP_401_UNAUTHORIZED)
            
            return Response({'success':True, 'message': 'Credenciales Validas', 'uidb64': uidb64, 'token': token}, status=status.HTTP_200_OK)
        except DjangoUnicodeDecodeError as identifier:
            return Response({'error':'Token invalido'}, status=status.HTTP_401_UNAUTHORIZED)

class SetNewPasswordAPIView(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'success':True, 'message': 'Contraseña cambiada correctamente'}, status=status.HTTP_200_OK)