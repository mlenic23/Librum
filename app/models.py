from django.db import models
from django.contrib.auth.models import User
from django.db.models import Avg
from django.utils import timezone

# Create your models here.

class Author(models.Model):
    name = models.TextField(null=True, blank=True)
    surname = models.TextField(null=True, blank=True)
    born = models.DateField(null=True, blank=True)
    place = models.TextField(null=True, blank=True)
    occupation = models.TextField(null=True, blank=True)
    genre = models.TextField(null=True, blank=True)
    notable_works = models.TextField(null=True, blank=True)
    achievements = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} {self.surname}"
    
    
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
        ('young adult', 'Young Adult'),
        ('humor', 'Humor'),
        ('adventure', 'Adventure'),
        ('autobiography', 'Autobiography'),
        ('science', 'Science'),
        ('psychology', 'Psychology'),
        ('other', 'Other')
    ]
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')
    genre = models.CharField(max_length=50, choices=GENRE_CHOICES)
    cover_image = models.ImageField(upload_to='books/covers')
    number_of_pages = models.PositiveIntegerField(null=True, blank=True)
    famous_quote = models.TextField(null=True, blank=True)
    summary = models.TextField(null=True, blank=True)
    published_date = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return self.title
    

    def average_rating(self):
        avg = self.ratings.aggregate(Avg('rating'))['rating__avg']
        return round(avg, 1) if avg is not None else 0


    def user_rating(self, user):
        rating = self.ratings.filter(user=user).first()
        return rating.rating if rating else None
    
class BookRating(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()

    class Meta:
        unique_together = ('book', 'user')

    def __str__(self):
        return f"{self.user.username} rated {self.book.title} ({self.rating})"

    
class Review(models.Model):
    book = models.ForeignKey('Book', on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} on {self.book.title}"
    
    def total_likes(self):
        return self.reviewlike_set.count()
    
    def is_liked_by(self,user):
        return self.reviewlike_set.filter(user=user).exists()
    
class ReviewLike(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('review', 'user')

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    wishlist_books = models.ManyToManyField(Book, related_name='favorited_by', blank=True)
    read_books = models.ManyToManyField(Book, related_name='read_by', blank=True)
    currently_reading_books = models.ManyToManyField(Book, related_name="currently_reading_by", blank=True)
    image = models.ImageField(upload_to='profile_pics', default='profile_pics/default.jpg')

    def __str__(self):
        return f"{self.user.username}'s Profile"

class ReadingProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    pages_read = models.PositiveIntegerField()
    date = models.DateField(default = timezone.now)

    class Meta:
        pass
    
    def __str__(self):
        return f"{self.user.username} read {self.pages_read} pages of {self.book.title} on {self.date}"