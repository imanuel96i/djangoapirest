# from django.conf.urls import url
from django.urls import path
from django.contrib import admin
from . import views
# from .admin import useradmin_site

admin.autodiscover()

urlpatterns = [
    # path('adminuser/', useradmin_site.urls),
    path('registro/', views.UserCreateAPIView.as_view(), name='registro'),
    path('verify/', views.VerifyEmail.as_view(), name='verify'),
    path('login/', views.LoginAPIView.as_view(), name='login'),
    path('request-reset-pw/', views.RequestPasswordReset.as_view(), name='request-reset-pw'),
    path('reset-password/<uidb64>/<token>', views.PasswordTokenCheckAPI.as_view(), name='reset-password-confirm'),
    path('reset-password-confirm/', views.SetNewPasswordAPIView.as_view(), name='reset-password-complete'),
]