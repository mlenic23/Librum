from django.contrib import admin
from .models import (
    Book,
    BookRating,
    Review,
    ReviewLike,
    UserProfile,
    ReadingProgress
)

admin.site.register(Book)
admin.site.register(BookRating)
admin.site.register(Review)
admin.site.register(ReviewLike)
admin.site.register(UserProfile)
admin.site.register(ReadingProgress)
