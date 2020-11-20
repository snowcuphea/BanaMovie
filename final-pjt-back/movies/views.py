import requests

from django.shortcuts import get_object_or_404
from django.core import serializers

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import MovieSerializer
from .models import Movie, Genre


@api_view(['GET'])
def getMovies(request):
    url = 'https://api.themoviedb.org/3/movie/popular?api_key=e8067ff017c9f1acd66ea2924205aae6'
    payload = {
        'language' : 'ko'
    }
    r = requests.get(url, params=payload)
    movies = r.json()
    original_data = Movie.objects.all()
    for movie in movies['results']:
        movie_new = Movie(
            movie_no= movie['id'],
            title= movie['title'],
            release_date= movie['release_date'],
            poster_path= movie['poster_path'],
            adult= movie['adult'],
            overview= movie['overview'],
        )
        movie_new.save(commit=False)

        for genre in movie['genre_ids']:
            movie_new.genres.add(genre)
        movie_new.save()
    completed_movies = Movie.objects.all()
    serialzed_movies = MovieSerializer(completed_movies, many=True)
    
    return Response(serialzed_movies.data)
    

