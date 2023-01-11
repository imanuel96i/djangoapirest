from django.urls import path, re_path
from django.contrib import admin
from django.conf.urls import include

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('rest_framework.urls', namespace='rest_framework')),
    path('api-auth/', include('Pelicula.urls')),
    # re_path(r'api-auth/^', include('Pelicula.urls'))
]