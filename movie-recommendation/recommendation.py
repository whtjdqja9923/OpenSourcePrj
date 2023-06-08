from flask import Blueprint, render_template
from movie_util import get_movie_details, get_similar_movieCds, get_top_n_movies_by_genre, get_top_n_movies_by_weighted_rating, movieCd_to_simple_info

movies_bp = Blueprint('movies_bp', __name__, url_prefix='/', template_folder="templates")

@movies_bp.route('/movies')
def recommendation_home():
    return render_template('recommendation_home.html')


@movies_bp.route('/movies/gnereal')
def general_recommendation():

    movieCds = get_top_n_movies_by_weighted_rating(5)
    simpleInfos = [movieCd_to_simple_info(movieCd) for movieCd in movieCds]

    return render_template('general_recommendation.html', simpleInfos=simpleInfos, movieCds=movieCds)


@movies_bp.route('/movies/<string:genre>')
def genre_recommendation(genre):

    movieCds = get_top_n_movies_by_genre(genre, 5)
    simpleInfos = [movieCd_to_simple_info(movieCd) for movieCd in movieCds]

    return render_template('genre_recommendation.html', simpleInfos=simpleInfos, movieCds=movieCds)

@movies_bp.route('/movies/<int:movieCd>')
def movie_detail(movieCd):
    movieRating, OpenDt, director, repGenreNm, movieNm, repNationNm, posterLink, comNm, synopsis = get_movie_details(movieCd)

    similar_movieCds, posterLinks = get_similar_movieCds(movieCd)

    return render_template('movie_detail.html', movieRating=movieRating, OpenDt=OpenDt, director=director, repGenreNm=repGenreNm, movieNm=movieNm, repNationNm=repNationNm, posterLink=posterLink, comNm=comNm, synopsis=synopsis, similar_movieCds=similar_movieCds, posterLinks=posterLinks)
