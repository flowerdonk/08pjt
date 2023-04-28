from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.views.decorators.http import require_safe, require_http_methods
from rest_framework.response import Response
from .models import Movie, Genre
from .serializers import GenreSerializer, MovieListSerializer, MovieSerializer, myReviewSerializer
from community.models import Review

# 영화 전체 조회
@require_safe
def index(request):
    movies = get_list_or_404(Movie)
    serializer = MovieListSerializer(movies, many=True)
    context = {
        'movies' : serializer.data,
    }
    return render(request, 'movies/index.html', context)
    

# 영화 상세 조회
# 기능: 영화 상세 조회 및 리뷰 확인, 리뷰 작성
@require_http_methods(['GET', 'POST'])
def detail(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    if request.method == 'GET':
        serializer = MovieSerializer(movie)
        context = {
            'movie' : serializer.data,
        }
    
    return render(request, 'movies/detail.html', context)


@require_safe
def recommended(request):

    # 제가 작성한 리뷰의 무비 id
    # mymovies = get_list_or_404(Review, user_id=request.user)
    myMovies = Review.objects.filter(user=request.user)
    print(myMovies)
    for m in myMovies:
        print(m.movie_id.genres_id.name)
    serializer = myReviewSerializer(myMovies, many=True)

    # data = serializer.data
    # genres = [item.pop('name') for item in data]
    # print('serializer.data', serializer.data)
    context = {
        # 'genres' : genres,
        'genres' : serializer.data,
    }
    return render(request, 'movies/recommended.html', context)