from django.urls import path, re_path
from django.contrib import admin
from django.conf.urls import include
from django.views.generic.base import RedirectView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('rest_framework.urls', namespace='rest_framework')),
    path('', RedirectView.as_view(url='api-auth/v2/')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api-auth/', include('Pelicula.urls')),
    path('api-auth/v2/', include('UserManagement.urls'))

    # re_path(r'api-auth/^', include('Pelicula.urls'))
]