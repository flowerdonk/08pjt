from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.views.decorators.http import require_safe, require_http_methods
from rest_framework.response import Response
from .models import Movie, Genre
from .serializers import GenreSerializer, MovieListSerializer, MovieSerializer, myReviewSerializer
from community.models import Review
import random


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

# 영화 추천 알고리즘
@require_safe
def recommended(request):

    # 해당 프로필 유저가 작성한 리뷰 목록
    myMovies = Review.objects.filter(user=request.user)


    ### [1] 작성한 리뷰가 있을 때
    if len(myMovies):
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
        

        # genre_list 내림차순 정렬
        genre_list = sorted(genre_list.items(), key=lambda x: x[1], reverse=True)
        # genre_max: 사용자가 가장 많은 리뷰를 작성한 장르 리스트
        genre_max  = [k for k,v in genre_list if genre_list[0][1] == v]
        # genre_choice: 가장 많은 리뷰를 생성한 장르가 여러 개 일때 랜덤하게 단 하나를 선택한다.
        genre_choice = random.choice(genre_max)
        # genre_chocie_num : 장르 이름으로 장르 테이블에서 객체를 검색 왜냐하면 장르 이름으로 장르 id를 뽑고 싶어서
        genre_chocie_num = Genre.objects.filter(name = genre_choice)
        
        for g in genre_chocie_num:
            g_id = g.id
    
        reco_movies = Movie.objects.filter(genres=g_id)

    ### [2] 작성한 리뷰가 없을 때
    else:
        # 장르 객체 전부 가져오기
        genres = get_list_or_404(Genre)
        # 장르 직렬화
        serializer = GenreSerializer(genres, many=True)
        data = serializer.data
        # 사용자가 작성한 리뷰가 없으므로, 모든 장르의 이름을 가져옴
        genre_max = [d.pop('name') for d in data]
        # 모든 장르 중에서 하나 선택
        genre_choice = random.choice(genre_max)
        # 해당 장르 이름으로 영화 선택
        genre_chocie_num = Genre.objects.filter(name = genre_choice)
        
        for g in genre_chocie_num:
            g_id = g.id

        reco_movies = Movie.objects.filter(genres=g_id)
    
    # 10개 이하로 추천영화 선별하기
    n = (min(10, len(reco_movies)))
    reco_movies = reco_movies[:n]
    context = {
        'genre_chocie' : genre_choice, # 추천하는 장르 한글 이름
        'reco_movies' : reco_movies, # 추천하는 장르 영화
            }

    return render(request, 'movies/recommended.html', context)