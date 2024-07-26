from django.shortcuts import render, get_object_or_404, redirect
from .models import Movie, Review
from .forms import MovieForm, ReviewForm
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import UserRegisterForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth import logout
from .forms import UserLoginForm

def movie_list(request):
    current_user=request.user
    movies = Movie.objects.all()
    return render(request, 'movies/movie_list.html', {'movies': movies,'user':current_user})

def movie_detail(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    reviews = Review.objects.filter(movie=movie)
    return render(request, 'movies/movie_detail.html', {'movie': movie, 'reviews': reviews})

def add_movie(request):
    if request.method == 'POST':
        form = MovieForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('movie_list')
    else:
        form = MovieForm()
    return render(request, 'movies/movie_form.html', {'form': form})

def add_review(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.movie = movie
            review.save()
            return redirect('movie_detail', pk=movie_id)
    else:
        form = ReviewForm()
    return render(request, 'movies/review_form.html', {'form': form,'movie':movie})

# def add_rating(request, movie_id):
#     movie = get_object_or_404(Movie, pk=movie_id)
#     if request.method == 'POST':
#         form = RatingForm(request.POST)
#         if form.is_valid():
#             rating = form.save(commit=False)
#             rating.user = request.user
#             rating.movie = movie
#             rating.save()
#             return redirect('movie_detail', pk=movie_id)
#     else:
#         form = RatingForm()
#     return render(request, 'movies/rating_form.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, f'Account created for {username}!')
            return redirect('movie_list')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = UserRegisterForm()
    return render(request, 'movies/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {username}!')
                return redirect('movie_list')
            else:
                if not User.objects.filter(username=username).exists():
                    messages.error(request, 'User does not exist.')
                else:
                    messages.error(request, 'Invalid password.')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = UserLoginForm()
    return render(request, 'movies/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')


