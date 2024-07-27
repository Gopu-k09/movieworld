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
from django.db.models import Q
from .forms import MovieSearchForm


def movie_list(request):
    current_user=request.user
    review=Review.objects.prefetch_related('movie').all()
    movies = Movie.objects.all()
    return render(request, 'movies/movie_list.html', {'movies': movies,'user':current_user})

def movie_detail(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    reviews = Review.objects.filter(movie=movie)
    average_rating=0
    total_review=reviews.count()
    if reviews:
        average_rating = round(sum(review.rating for review in reviews) / reviews.count(),2)
    return render(request, 'movies/movie_detail.html', {'movie': movie, 'reviews': reviews,'avg_rating':average_rating,'total':total_review})

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


def movie_search(request):
    form = MovieSearchForm()
    query = None
    results = []
    if 'query' in request.GET:
        form = MovieSearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            results = Movie.objects.filter(
                Q(title__icontains=query) |
                Q(director__icontains=query) |
                Q(cast__icontains=query)|
                Q(release_date__icontains=query)|
                Q(genre__icontains=query)|
                Q(description__icontains=query)
            )
    return render(request, 'movies/movie_search.html', {'form': form, 'query': query, 'results': results})
