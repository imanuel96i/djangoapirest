from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import Pelicula, Genre

# class UserSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = User
#         fields = ['url', 'username', 'email', 'groups']


# class GroupSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = Group
#         fields = ['url', 'name']

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('__all__')
        read_only_fields = ('date_created', )

class PeliculaSerializer(serializers.ModelSerializer):
    # genre = serializers.PrimaryKeyRelatedField(queryset=Genre.objects.all(), write_only=True)
    # genre = GenreSerializer
    genre = serializers.SlugRelatedField(queryset=Genre.objects.all(), slug_field='title')

    class Meta:
        model   = Pelicula
        fields  = ('id', 'title', 'description', 'genre', 'date_published')
        # depth   = 1