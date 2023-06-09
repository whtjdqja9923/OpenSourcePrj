from flask import Blueprint, render_template, Flask
from movie_recommendation.movie_util import get_movie_details, get_similar_movieCds, get_top_n_movies_by_genre, get_top_n_movies_by_weighted_rating, movieCd_to_simple_info

mr = Blueprint('mr', __name__, url_prefix='/recommendation')

@mr.route('/')
def recommendation_home():
    return render_template('recommendation_home.html')


@mr.route('/gnereal')
def general_recommendation():

    movieCds = get_top_n_movies_by_weighted_rating(5)
    simpleInfos = [movieCd_to_simple_info(movieCd) for movieCd in movieCds]

    return render_template('general_recommendation.html', simpleInfos=simpleInfos, movieCds=movieCds)


@mr.route('/<string:genre>')
def genre_recommendation(genre):

    movieCds = get_top_n_movies_by_genre(genre, 5)
    simpleInfos = [movieCd_to_simple_info(movieCd) for movieCd in movieCds]

    return render_template('genre_recommendation.html', simpleInfos=simpleInfos, movieCds=movieCds)

@mr.route('/<int:movieCd>')
def movie_detail(movieCd):
    movieRating, OpenDt, director, repGenreNm, movieNm, repNationNm, posterLink, comNm, synopsis = get_movie_details(movieCd)

    similar_movieCds, posterLinks = get_similar_movieCds(movieCd)

    return render_template('movie_detail.html', movieRating=movieRating, OpenDt=OpenDt, director=director, repGenreNm=repGenreNm, movieNm=movieNm, repNationNm=repNationNm, posterLink=posterLink, comNm=comNm, synopsis=synopsis, similar_movieCds=similar_movieCds, posterLinks=posterLinks)
