from flask import Blueprint, render_template
from . import movie_util

movies_bp = Blueprint('movies_bp', __name__, url_prefix='/', template_folder="templates")


# weighted rating 기준 영화추천 페이지
@movies_bp.route('/movies')
def movie_recommendation_list():
    # weighted rating 기준 상위 10개 영화 반환
    return render_template('movie_recommendation_list.html', top_n_movie=movie_util.get_top_n_movies_by_weighted_rating(10))


# 장르별 영화추천 페이지
@movies_bp.route('/movies/<string:genre>')
def movies_by_genre(genre):
    # 장르별 weightedRating 기준 상위 n개 영화 출력
    return render_template('movies_by_genre.html', genre=genre, top_n_movies=movie_util.get_top_n_movies_by_genre(genre, 10))


# 영화 상세정보 페이지
@movies_bp.route('/movies/<int:movieCd>')
def movie_detail(movieCd):

    actors, movieRating, prdtYear, openDt, directors, repGenreNm, movieNmEng= movie_util.get_movie_details(movieCd)

    # 선택한 영화의 movieCd에 해당하는 영화 정보 및 유사한 영화목록 반환
    return render_template('movie_detail.html', movieNmEng=movieNmEng, movieRating=movieRating, prdtYear=prdtYear, openDt=openDt, repGenreNm=repGenreNm, actors=actors, directors=directors)
