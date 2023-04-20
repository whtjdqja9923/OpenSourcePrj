from flask import Blueprint, render_template
from . import movie_util

movies_bp = Blueprint('movies_bp', __name__, template_folder="templates")


# 추천 영화목록 출력
@movies_bp.route('/movies')
def movie_detail():
    # 사용자 정보에 따라 추천 영화목록 반환
    return render_template('movie_recommendation_list.html', movie_recommendation_list=movie_util.get_movie_recommendation_list())


# 영화 정보 및 연관 영화 출력
@movies_bp.route('/movies/<int:movie_id>')
def movie_detail(movie_id):
    # 선택한 영화의 movie_id에 해당하는 영화 정보 및 연관 영화 반환
    return render_template('movie_detail.html', movie_title=movie_util.get_title_by_id(movie_id), movie_rating=movie_util.get_rating_by_id(movie_id))