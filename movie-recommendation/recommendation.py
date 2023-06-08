from flask import Blueprint, render_template
from . import movie_util

movies_bp = Blueprint('movies_bp', __name__, url_prefix='/', template_folder="templates")

@movies_bp.route('/movies')
def movie_recommendation_list():

    movieCds = movie_util.get_top_n_movies_by_weighted_rating(10)
    movieNms = [movie_util.movieCd_to_movieNmEng(movieCd) for movieCd in movieCds]

    return render_template('movie_recommendation_list.html', movieNms=movieNms, movieCds=movieCds)


@movies_bp.route('/movies/<string:genre>')
def movie_recommendation_list_by_genre(genre):

    movieCds = movie_util.get_top_n_movies_by_genre(genre, 10)
    movieNms = [movie_util.movieCd_to_movieNmEng(movieCd) for movieCd in movieCds]

    return render_template('movie_recommendation_list.html', movieNms=movieNms, movieCds=movieCds)


@movies_bp.route('/movies/<int:movieCd>')
def movie_detail(movieCd):

     = movie_util.get_movie_details(movieCd)

    return render_template('movie_detail.html', )
