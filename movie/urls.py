from django.urls import path
from . import views

urlpatterns = [
    path('', views.movie_list, name='movie_list'),
    path('movie/<int:pk>/', views.movie_detail, name='movie_detail'),
    path('movie/add/', views.add_movie, name='add_movie'),
    path('movie/<int:movie_id>/review/', views.add_review, name='add_review'),
    path('movie/<int:movie_id>/rating/', views.add_rating, name='add_rating'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
