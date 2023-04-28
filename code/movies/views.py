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

    # 해당 프로필 유저가 작성한 리뷰 목록
    myMovies = Review.objects.filter(user=request.user)

    # 해당 유저가 작성한 리뷰들의 장르 값을 담을 딕셔너리 {'장르': 작성한 리뷰 수}
    genre_list = dict()

    # 리뷰 목록을 돌며 장르 가져오기
    for m in myMovies: 
        movie_id = Movie.objects.get(pk=m.movie_id.pk) # 해당 리뷰 하나의 영화 id
        genre_obj = Genre.objects.filter(movie = movie_id) # 해당 영화 id의 장르 객체 반환
        for g in genre_obj: # 해당 영화의 장르가 여러개일 수 있어서 반복문 사용
            if g.name not in genre_list.keys(): # 딕셔너리에 해당 장르가 없으면 키 추가
                genre_list[g.name] = 1
            else: # 딕셔너리에 해당 장르가 있으면 값 추가
                genre_list[g.name] += 1

    context = {
        'genre_list' : genre_list,
    }
    return render(request, 'movies/recommended.html', context)