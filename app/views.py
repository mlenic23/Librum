from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django import forms
from .models import Book, Review, ReviewLike, BookRating, UserProfile, ReadingProgress
from .forms import CustomUserCreationForm, ReviewForm, RatingForm
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

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

def book_list(request):
    query = request.GET.get('q')  
    selected_genres = request.GET.getlist('genre')  
    sort = request.GET.get('sort')  

    books = Book.objects.all()

    if query:
        books = books.filter(Q(title__icontains=query) | Q(author__icontains=query))

    if selected_genres:
        genre_map = {display: value for value, display in Book.GENRE_CHOICES}
        db_genres = [genre_map.get(genre) for genre in selected_genres if genre in genre_map]
        if db_genres:
            books = books.filter(genre__in=db_genres)

    if sort == 'asc':
        books = books.order_by('title')
    elif sort == 'desc':
        books = books.order_by('-title')

    paginator = Paginator(books, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
   
    all_genres = [genre[1] for genre in Book.GENRE_CHOICES]

    return render(request, 'book_list.html', {
        'books': page_obj.object_list,
        'page_obj': page_obj,
        'genres': all_genres,
        'selected_genres': selected_genres,
        'sort': sort,  
    })

from django.db.models import Avg
from django.contrib.auth.decorators import login_required

@login_required  # ako želiš da rating/review zahtijeva login
def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    reviews = book.reviews.all().order_by('-created_at')

    # Označi koje recenzije je korisnik lajkao
    for review in reviews:
        review.user_liked = review.is_liked_by(request.user)

    # Dohvati korisnikovu ocjenu, ako postoji
    user_rating = None
    existing_rating = BookRating.objects.filter(book=book, user=request.user).first()
    if existing_rating:
        user_rating = existing_rating.rating

    # Inicijalni formovi
    review_form = ReviewForm()
    rating_form = RatingForm(initial={'rating': user_rating})

    if request.method == 'POST':
        # Ako korisnik šalje ocjenu (bez gumba, preko JS ili onchange)
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
                # Dodavanje recenzije
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
        'rating_range': [5, 4, 3, 2, 1],  # Dodano da znaš korisnikovu ocjenu u template-u
    })



@login_required
def toggle_review_like(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    like, created = ReviewLike.objects.get_or_create(user=request.user, review=review)
    if not created:
        like.delete()
    return redirect('book_detail', book_id=review.book.id)


@login_required
def user_profile(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    favorite_books = profile.favorite_books.all()
    read_books = profile.read_books.all()
    reading_progress = ReadingProgress.objects.filter(user=request.user)

    return render(request, 'user_profile.html',{
        'favorite_books':favorite_books,
        'read_books':read_books,
        'reading_progress':reading_progress
    })

@login_required
def toggle_favorite_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    if book in profile.favorite_books.all():
        profile.favorite_books.remove(book)
    else:
        profile.favorite_books.add(book)
    return redirect('user_profile')

@login_required
def mark_book_read(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    if book not in profile.read_books.all():
        profile.read_books.add(book)
        # Optionally, mark full progress if marking as read
        progress, created = ReadingProgress.objects.get_or_create(user=request.user, book=book)
        if book.number_of_pages:
            progress.pages_read = book.number_of_pages
            progress.save()
    return redirect('user_profile')

@login_required
def update_reading_progress(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        pages_read = request.POST.get('pages_read')
        try:
            pages_read = int(pages_read)
            if pages_read >= 0 and (not book.number_of_pages or pages_read <= book.number_of_pages):
                progress, created = ReadingProgress.objects.get_or_create(user=request.user, book=book)
                progress.pages_read = pages_read
                progress.save()
                if book.number_of_pages and pages_read == book.number_of_pages:
                    profile, created = UserProfile.objects.get_or_create(user=request.user)
                    profile.read_books.add(book)
                return redirect('user_profile')
            else:
                messages.error(request, 'Invalid page number.')
        except ValueError:
            messages.error(request, 'Please enter a valid number.')
    return redirect('user_profile')