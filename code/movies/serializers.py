from rest_framework import serializers
from .models import Genre, Movie
from community.models import Review

class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = '__all__'

# index 페이지
class MovieListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Movie
        fields = ('id', 'title', 'poster_path', )

# detail 페이지
class MovieSerializer(serializers.ModelSerializer):
    reviews = serializers.SerializerMethodField()
    genres = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = ('title', 'popularity', 'vote_count', 'vote_average', 'overview', 'poster_path', 'genres', 'reviews', 'id', 'release_date', )
        # fields = '__all__'
        
    # reviews 추가
    def get_reviews(self, movie):
        reviews = movie.review_set.all()
        return [{'title': review.title, 'content': review.content, 'rank':review.rank, } for review in reviews]
    
    def get_genres(self, movie):
        genres_obj = Genre.objects.filter(movie = movie)
        genres = []
        for g in genres_obj:
            genres.append(g.name)
        return genres

class myReviewSerializer(serializers.ModelSerializer):
    # genre = serializers.SerializerMethodField()


    class Meta:
        model = Review
        # fields = ('genre',)
        fields = '__all__'

    # def get_genre(self, review):
    #     movie = review.movie_id
    #     print(movie.genres)
     
    #     return movie.genres