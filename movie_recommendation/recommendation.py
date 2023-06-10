from flask import Blueprint, render_template, Flask, request, redirect
from movie_recommendation.movie_util import get_movie_details, get_similar_movieCds, get_top_n_movies_by_genre, get_top_n_movies_by_weighted_rating, movieCd_to_simple_info

mr = Blueprint('mr', __name__, url_prefix='/recommendation')

@mr.route('/')
def recommendation_home():
    return render_template('recommendation_home.html')


@mr.route('/general')
def general_recommendation():

    movieCds = get_top_n_movies_by_weighted_rating(10)
    simpleInfos = [movieCd_to_simple_info(movieCd) for movieCd in movieCds]

    return render_template('general_recommendation.html', simpleInfos=simpleInfos, movieCds=movieCds)

@mr.route('/genre/<string:genre>')
def genre_recommendation(genre):
    if genre == '멜로':
        genre = '멜로/로맨스'
        
    movieCds = get_top_n_movies_by_genre(genre, 10)
    simpleInfos = [movieCd_to_simple_info(movieCd) for movieCd in movieCds]

    return render_template('genre_recommendation.html', simpleInfos=simpleInfos, movieCds=movieCds)

@mr.route('/<string:movieCd>')
def movie_detail(movieCd):
    detailInfo = get_movie_details(movieCd)

    movieCds, posterLinks = get_similar_movieCds(movieCd)

    return render_template('movie_detail.html', detailInfo=detailInfo, movieCds=movieCds, posterLinks=posterLinks)
