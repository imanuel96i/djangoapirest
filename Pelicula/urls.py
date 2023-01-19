from django.conf.urls import include
from django.urls import path
from django.contrib import admin
from . import views
from rest_framework import routers

admin.autodiscover()

router = routers.SimpleRouter()
# router.register(r'users', views.UserViewSet)
# router.register(r'groups', views.GroupViewSet)
router.register(r'peliculas', views.PeliculaViewSet)
router.register(r'categorias', views.CategoryViewSet)



# urlpatterns = [
#     # path('', include(router.urls)),
#     path('peliculas/', views.PeliculaList.as_view()),
#     path('peliculas/<int:pk>', views.PeliculaDetail.as_view()),
#     path('categorias/', views.CategoryList.as_view()),
#     path('categorias/<int:pk>', views.CategoryDetail.as_view()),
#     path('v2/', include(router.urls))
# ]