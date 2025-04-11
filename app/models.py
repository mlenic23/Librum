from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Book(models.Model):
    GENRE_CHOICES = [
        ('fantasy', 'Fantasy'),
        ('sci-fi', 'Sci-Fi'),
        ('romance', 'Romance'),
        ('mystery', 'Mystery'),
        ('history', 'History'),
        ('drama', 'Drama'),
        ('thriller', 'Thriller'),
        ('religion', 'Religion'),
        ('crime', 'Crime'),
        ('action', 'Action'),
        ('humor', 'Humor'),
        ('adventure', 'Adventure'),
        ('autobiography', 'Autobiography'),
        ('cookbook', 'Cookbook'),
        ('psychology', 'Psychology'),
        ('other', 'Other')
    ]
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    genre = models.CharField(max_length=50, choices=GENRE_CHOICES)
    cover_image = models.ImageField(upload_to='books/covers')

    def __str__(self):
        return self.title
    
