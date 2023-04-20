from flask import Blueprint, render_template
from . import movie_util

movies_bp = Blueprint('movies_bp', __name__, template_folder="templates")


# ��õ ��ȭ��� ���
@movies_bp.route('/movies')
def movie_detail():
    # ����� ������ ���� ��õ ��ȭ��� ��ȯ
    return render_template('movie_recommendation_list.html', movie_recommendation_list=movie_util.get_movie_recommendation_list())


# ��ȭ ���� �� ���� ��ȭ ���
@movies_bp.route('/movies/<int:movie_id>')
def movie_detail(movie_id):
    # ������ ��ȭ�� movie_id�� �ش��ϴ� ��ȭ ���� �� ���� ��ȭ ��ȯ
    return render_template('movie_detail.html', movie_title=movie_util.get_title_by_id(movie_id), movie_rating=movie_util.get_rating_by_id(movie_id))