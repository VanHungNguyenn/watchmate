from django.contrib import admin
from django.urls import include, path

# from watchlist_app.api.views import movie_details, movie_list
from watchlist_app.api.views import MovieListAV, MovieDetailAV

urlpatterns = [
    path("list/", MovieListAV.as_view(), name="movie-list"),
    path("<int:pk>/", MovieDetailAV.as_view(), name="movie-details"),
]
