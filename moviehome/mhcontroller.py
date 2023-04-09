from flask import Blueprint, render_template

# 블루프린트 생성
mh = Blueprint('m_home', __name__, url_prefix='/', template_folder="templates")

# 컨트롤러 작성
@mh.route('/')
def index():
    return render_template("index.html")