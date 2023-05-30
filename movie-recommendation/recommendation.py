from flask import Blueprint, render_template
from . import movie_util

movies_bp = Blueprint('movies_bp', __name__, url_prefix='/', template_folder="templates")


# weighted rating ���� ��ȭ��õ ������
@movies_bp.route('/movies')
def movie_recommendation_list():
    # weighted rating ���� ���� 10�� ��ȭ ��ȯ
    return render_template('movie_recommendation_list.html', top_n_movie=movie_util.get_top_n_movies_by_weighted_rating(10))


# �帣�� ��ȭ��õ ������
@movies_bp.route('/movies/<string:genre>')
def movies_by_genre(genre):
    # �帣�� weightedRating ���� ���� n�� ��ȭ ���
    return render_template('movies_by_genre.html', genre=genre, top_n_movies=movie_util.get_top_n_movies_by_genre(genre, 10))


# ��ȭ ������ ������
@movies_bp.route('/movies/<int:movieCd>')
def movie_detail(movieCd):

    actors, movieRating, prdtYear, openDt, directors, repGenreNm, movieNmEng= movie_util.get_movie_details(movieCd)

    # ������ ��ȭ�� movieCd�� �ش��ϴ� ��ȭ ���� �� ������ ��ȭ��� ��ȯ
    return render_template('movie_detail.html', movieNmEng=movieNmEng, movieRating=movieRating, prdtYear=prdtYear, openDt=openDt, repGenreNm=repGenreNm, actors=actors, directors=directors)
