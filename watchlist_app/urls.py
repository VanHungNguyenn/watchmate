from django.contrib import admin
from django.urls import include, path

from watchlist_app.views import movie_details, movie_list

urlpatterns = [
    path("list/", movie_list, name="movie-list"),
    path("<int:pk>/", movie_details, name="movie-details"),
]
