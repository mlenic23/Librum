from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django import forms
from .models import Book, Review, ReviewLike, BookRating, UserProfile, ReadingProgress
from .forms import CustomUserCreationForm, ReviewForm, RatingForm
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import LabelEncoder
from django.http import JsonResponse
import pandas as pd
from django.db.models import Avg, Sum, Count
from django.utils import timezone
from django.db.models.functions import ExtractYear
from sklearn.preprocessing import LabelEncoder

def home(request):
    return render(request, 'home.html')

def user_register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successful registration!')
            return redirect('login')
        else:
            messages.error(request, 'Please fill out all registration fields!')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Wrong username or password.')
    return render(request, 'login.html')

def user_logout(request):
    logout(request)
    return redirect('login')

def clean_email(self):
    email = self.cleaned_data.get('email')
    if User.objects.filter(email=email).exists():
        raise forms.ValidationError("Email is already in use.")
    return email

def search_books(request):
    query = request.GET.get('q', '').strip()
    books = Book.objects.all().annotate(published_year=ExtractYear('published_date'))

    if query:
        terms = query.lower().split()
        conditions = Q()

        for term in terms:
            if term.isdigit() and 1000 <= int(term) <= 2025:  
                year = int(term)
                conditions &= Q(published_year=year)

            elif term.isdigit():  
                pages = int(term)
                conditions &= Q(number_of_pages__gte=max(0, pages - 50)) & Q(number_of_pages__lte=pages + 50)

            elif not any(char.isdigit() for char in term):
                text_condition = (
                    Q(author__icontains=term) &
                    Q(title__icontains=term) &
                    Q(genre__icontains=term)
                )
                text_condition = (
                    Q(author__icontains=term) |
                    Q(title__icontains=term) |
                    Q(genre__icontains=term)
                )
                conditions &= text_condition

        books = books.filter(conditions).filter(published_date__isnull=False)

    return {
        'books': books,
        'query': query,
    }

def filter_books(request, search_data=None):
    if search_data is None:
        books = Book.objects.all().annotate(published_year=ExtractYear('published_date'))
    else:
        books = search_data['books']

    selected_genres = request.GET.getlist('genre')
    sort = request.GET.get('sort')
    min_pages = request.GET.get('min_pages')
    max_pages = request.GET.get('max_pages')
    min_year = request.GET.get('min_year')
    max_year = request.GET.get('max_year')
    selected_author = request.GET.get('author')

    if selected_genres:
        genre_map = {display: value for value, display in Book.GENRE_CHOICES}
        db_genres = [genre_map.get(genre) for genre in selected_genres if genre in genre_map]
        if db_genres:
            books = books.filter(genre__in=db_genres)

    if min_pages and max_pages:
        try:
            min_pages = int(min_pages)
            max_pages = int(max_pages)
            if min_pages > max_pages:
                min_pages, max_pages = max_pages, min_pages  
        except ValueError:
            min_pages = max_pages = None  
    elif min_pages:
        min_pages = int(min_pages)
    elif max_pages:
        max_pages = int(max_pages)

    if min_pages:
        books = books.filter(number_of_pages__gte=min_pages)

    if max_pages:
        books = books.filter(number_of_pages__lte=max_pages)

    if min_year:
        books = books.filter(published_year__gte=min_year)

    if max_year:
        books = books.filter(published_year__lte=max_year)

    if selected_author:
        books = books.filter(author=selected_author)

    books = books.annotate(avg_rating=Avg('ratings__rating'))

    if sort == 'asc':
        books = books.order_by('title')
    elif sort == 'desc':
        books = books.order_by('-title')
    elif sort == 'rating_desc':
         books = books.order_by('-avg_rating')
    elif sort == 'rating_asc':
        books = books.order_by('avg_rating')
 


    paginator = Paginator(books, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    all_genres = [genre[1] for genre in Book.GENRE_CHOICES]
    all_authors = Book.objects.values_list('author', flat=True).distinct()

    return render(request, 'book_list.html', {
        'books': page_obj.object_list,
        'page_obj': page_obj,
        'genres': all_genres,
        'selected_genres': selected_genres,
        'sort': sort,
        'min_pages': min_pages,
        'max_pages': max_pages,
        'min_year': min_year,
        'max_year': max_year,
        'selected_author': selected_author,
        'authors': all_authors,
        'query': search_data['query'] if search_data else '',
    })

def book_list(request):
    search_data = search_books(request)
    return filter_books(request, search_data)


@login_required
def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    reviews = book.reviews.all().order_by('-created_at')

    user_profile, created = UserProfile.objects.get_or_create(user=request.user)

    for review in reviews:
        review.user_liked = review.is_liked_by(request.user)

    user_rating = None
    existing_rating = BookRating.objects.filter(book=book, user=request.user).first()
    if existing_rating:
        user_rating = existing_rating.rating

    review_form = ReviewForm()
    rating_form = RatingForm(initial={'rating': user_rating})

    if request.method == 'POST':
        if 'rating' in request.POST and not existing_rating:
            rating_form = RatingForm(request.POST)
            if rating_form.is_valid():
                rating_value = int(rating_form.cleaned_data['rating'])
                BookRating.objects.create(
                    book=book,
                    user=request.user,
                    rating=rating_value
                )
                avg_rating = BookRating.objects.filter(book=book).aggregate(Avg('rating'))['rating__avg']
                book.average_rating = round(avg_rating, 2) if avg_rating else 0
                book.save()
                return redirect('book_detail', book_id=book.id)

        if 'review_submit' in request.POST:
            review_form = ReviewForm(request.POST)
            if review_form.is_valid():
                review = review_form.save(commit=False)
                review.user = request.user
                review.book = book
                review.save()
                return redirect('book_detail', book_id=book.id)

    return render(request, 'book_detail.html', {
        'book': book,
        'reviews': reviews,
        'form': review_form,
        'rating_form': rating_form,
        'user_rating': user_rating,
        'rating_range': [5, 4, 3, 2, 1],
    })


@login_required
def toggle_review_like(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    like, created = ReviewLike.objects.get_or_create(user=request.user, review=review)
    if not created:
        like.delete()
    return redirect('book_detail', book_id=review.book.id)

@login_required
def user_profile(request, user_id):
    target_user = get_object_or_404(User, id=user_id)
    profile = get_object_or_404(UserProfile, user=target_user)

    favorite_books = profile.favorite_books.all()
    currently_reading_books = profile.currently_reading_books.all()
    read_books = profile.read_books.all()
    
    recommended_books = recommend_books_knn(request.user)

    total_pages = profile.read_books.aggregate(total=Sum('number_of_pages'))['total'] or 0
    genre_counts = profile.read_books.values('genre').annotate(count=Count('id')).order_by('-count').first()
    top_genre = genre_counts['genre'] if genre_counts else 'N/A'
    author_counts = profile.read_books.values('author').annotate(count=Count('id')).order_by('-count').first()
    top_author = author_counts['author'] if author_counts else 'N/A'

    top_rated_books = (
        profile.read_books
        .annotate(avg_rating=Avg('ratings__rating'))
        .order_by('-avg_rating')[:4]
    )

    return render(request, 'user_profile.html', {
        'user_profile': profile,
        'target_user': target_user,
        'favorite_books': favorite_books,
        'read_books': read_books,
        'recommended_books': recommended_books,
        'total_pages': total_pages,
        'genre_counts': genre_counts,
        'top_genre': top_genre,
        'top_author': top_author,
        'currently_reading_books': currently_reading_books,
        'top_rated_books': top_rated_books,
    })


@login_required
def my_profile_redirect(request):
    return redirect('user_profile', user_id=request.user.id)

@login_required
def toggle_favorite_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    user_profile = get_object_or_404(UserProfile, user=request.user)
    if book in user_profile.favorite_books.all():
        user_profile.favorite_books.remove(book)
    else:
        user_profile.favorite_books.add(book)
    return redirect('user_profile')

@login_required
def mark_book_read(request, book_id):
    if request.method == "POST":
        user_profile = get_object_or_404(UserProfile, user=request.user)
        book = get_object_or_404(Book, id=book_id)
        if book not in user_profile.read_books.all():
         user_profile.read_books.add(book)
        if book in user_profile.favorite_books.all():
         user_profile.favorite_books.remove(book)

        return redirect('user_profile')
    return redirect('user_profile')

@login_required
def currently_reading_books(request, book_id):
    if request.method == "POST":
        book = get_object_or_404(Book, id=book_id)
        user_profile = get_object_or_404(UserProfile, user=request.user)

        if book not in user_profile.currently_reading_books.all():
            user_profile.currently_reading_books.add(book)
        
        if book in user_profile.favorite_books.all():
            user_profile.favorite_books.remove(book)
        
        if book in user_profile.read_books.all():
            user_profile.read_books.remove(book)
        
        return redirect('user_profile')
    return redirect('user_profile')


@login_required
def log_reading_progress(request, book_id):
    if request.method == 'POST':
        book = get_object_or_404(Book, id=book_id)
        user_profile = get_object_or_404(UserProfile, user=request.user)

        try:
            pages_read = int(request.POST.get('pages_read', 0))
        except (ValueError, TypeError):
            return JsonResponse({'status': 'error', 'message': 'Invalid number of pages'}, status=400)

        if pages_read < 0:
            return JsonResponse({'status': 'error', 'message': 'Pages read cannot be negative'}, status=400)

        ReadingProgress.objects.create(
            user=request.user,
            book=book,
            pages_read=pages_read,
            date=timezone.now().date()
        )

        total_pages_read = ReadingProgress.objects.filter(user=request.user, book=book).aggregate(total=Sum('pages_read'))['total'] or 0

        if total_pages_read >= book.number_of_pages:
            if book in user_profile.currently_reading_books.all():
                user_profile.currently_reading_books.remove(book)
                user_profile.read_books.add(book)

        return JsonResponse({'status': 'success'})
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)


def recommend_books_knn(user, n_recommendations=5):
    books = Book.objects.all().values('id', 'title', 'genre', 'author', 'number_of_pages')
    books_df = pd.DataFrame(books)

    books_df['average_rating'] = [Book.objects.get(id=book_id).average_rating() for book_id in books_df['id']]

    genre_encoder = LabelEncoder()
    author_encoder = LabelEncoder()
    
    books_df['genre_encoded'] = genre_encoder.fit_transform(books_df['genre'])
    books_df['author_encoded'] = author_encoder.fit_transform(books_df['author'])
    books_df['average_rating'] = books_df['average_rating'].fillna(books_df['average_rating'].mean())
    books_df['number_of_pages'] = books_df['number_of_pages'].fillna(books_df['number_of_pages'].mean())

    features = books_df[['genre_encoded', 'author_encoded', 'number_of_pages', 'average_rating']].values

    try:
        user_profile = UserProfile.objects.get(user=user)
        read_books = user_profile.read_books.values_list('id', flat=True)
    except UserProfile.DoesNotExist:
        read_books = []
    read_books_ids = set(read_books)

    if not read_books:
        return Book.objects.all().order_by('?')[:n_recommendations]

    read_books_data = books_df[books_df['id'].isin(read_books_ids)]
    read_books_features = read_books_data[['genre_encoded', 'author_encoded', 'number_of_pages', 'average_rating']].values
    total_samples = len(books_df)
    n_neighbors = min(n_recommendations + len(read_books_ids), total_samples)

    knn = NearestNeighbors(n_neighbors=n_neighbors, metric='cosine')
    knn.fit(features)

    recommendations = set()
    for book_features in read_books_features:
        distances, indices = knn.kneighbors([book_features])
        for idx in indices[0]:
            book_id = books_df.iloc[idx]['id']
            if book_id not in read_books_ids:
                recommendations.add(book_id)
    if len(recommendations) < n_recommendations:
        extra_books = Book.objects.exclude(id__in=read_books_ids).exclude(id__in=recommendations).order_by('?')[:n_recommendations - len(recommendations)]
        recommendations.update(extra_books.values_list('id', flat=True))
    recommended_books = Book.objects.filter(id__in=list(recommendations)[:n_recommendations])
    return recommended_books

from django.db.models import Sum

@login_required
def total_reading_progress(request, book_id):
    total_read = ReadingProgress.objects.filter(user=request.user, book_id=book_id).aggregate(total=Sum('pages_read'))['total'] or 0
    return JsonResponse({'total_read': total_read})


@login_required
def upload_profile_image(request):
    if request.method == 'POST':
        profile = request.user.userprofile
        if 'image' in request.FILES:
            profile.image = request.FILES['image']
            profile.save()
        return redirect('user_profile') 
    return redirect('user_profile')
