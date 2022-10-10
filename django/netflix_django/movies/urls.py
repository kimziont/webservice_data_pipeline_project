from django.urls import path
from . import views

urlpatterns = [
    path('index/', views.index),
    path('movie-create/', views.MovieCreateView.as_view(), name='movie-create'),
    path('movie-form/', views.MovieListView.as_view()),
    path('movie-list/', views.MovieListView.as_view(), name='movie-list'),
    path('my-movie-list/', views.FavoriteMovieListView.as_view(), name='favorite-movie-list'),
    path('movie-detail/<int:movie_id>', views.MovieDetailView.as_view(), name='movie-detail'),
    path('comment-create/', views.CommentCreateView.as_view(), name='comment-create'),
    path('movie-play/<int:id>', views.moviePlay, name='movie-play')
]