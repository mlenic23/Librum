from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import CustomUserCreationForm, BookForm
from django.contrib import messages
from django.contrib.auth.models import User
from django import forms
from .models import Book
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator

# Create your views here.

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
    return render(request, 'register.html', {'form':form})

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

    books = Book.objects.all()

    if query:
        books = books.filter(Q(title__icontains=query) | Q(author__icontains=query))
    
    if selected_genres:
        genre_map = {display: value for value, display in Book.GENRE_CHOICES}
        db_genres = [genre_map.get(genre) for genre in selected_genres if genre in genre_map]
        if db_genres:
            books = books.filter(genre__in=db_genres)

    paginator = Paginator(books, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
   
    all_genres = [genre[1] for genre in Book.GENRE_CHOICES]

    return render(request, 'book_list.html', {
        'books': page_obj.object_list, 
        'page_obj':page_obj,
        'genres': all_genres,
        'selected_genres': selected_genres,
    })

def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    return render(request, 'book_detail.html', {'book':book})

def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('book_list')  
    else:
        form = BookForm()
    
    return render(request, 'add_book.html', {'form': form})