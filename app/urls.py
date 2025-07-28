from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.user_register, name='register'),
    path('books/', views.book_list, name='book_list'),
    path('books/<int:book_id>/', views.book_detail, name='book_detail'),
    path('review/<int:review_id>/like/', views.toggle_review_like, name='toggle_review_like'),
    path('books/<int:book_id>/wishlist/', views.wishlist_book, name='wishlist_book'),
    path('books/<int:book_id>/mark-read/', views.mark_book_read, name='mark_book_read'),
    path('books/<int:book_id>/currently-reading/', views.currently_reading_books, name='currently_reading_books'),
    path('books/<int:book_id>/log-progress/', views.log_reading_progress, name='log_reading_progress'),
    path('books/<int:book_id>/total-progress/', views.total_reading_progress, name='total_reading_progress'),
    path('upload-profile-image/', views.upload_profile_image, name='upload_profile_image'),
    path('profile/<int:user_id>/', views.user_profile, name='user_profile'),
    path('profile/', views.my_profile_redirect, name='my_profile'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)