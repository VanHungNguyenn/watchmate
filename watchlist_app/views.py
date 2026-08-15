from django.http import JsonResponse
from django.shortcuts import render
from watchlist_app.models import Movie


# Create your views here.
def movie_list(request):
    movies = Movie.objects.all()
    print(movies.values())
    data = list(movies.values())

    return JsonResponse(data, safe=False)
