from django.db import models
from django.utils import timezone

class Genre(models.Model):
    id              = models.AutoField(unique=True, primary_key=True)
    title           = models.CharField(max_length=100)
    date_created    = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

class Pelicula(models.Model):
    id              = models.AutoField(unique=True, primary_key=True)
    title           = models.CharField(max_length=100)
    description     = models.CharField(max_length=255)
    date_published  = models.DateField(blank=True)
    genre           = models.ForeignKey(Genre, related_name='genre_relatives', on_delete=models.PROTECT)

    def __str__(self):
        return self.title, self.description, self.genre, self.date_published
