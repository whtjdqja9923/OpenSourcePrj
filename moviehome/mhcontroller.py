from flask import Blueprint, render_template

# 블루프린트 생성
mh = Blueprint('m_home', __name__, url_prefix='/', template_folder="templates")

# 컨트롤러 작성

#메인페이지
@mh.route('/')
def index():
    return render_template("index.html")

#회원가입 페이지(폼)
@mh.route('/signup')
def signup():
    return "회원가입 신청 페이지"

#회원가입 정보를 입력받아 가입처리
@mh.route('/signup/register', methods = ['POST'])
def signup_request():
    return "회원가입 처리로직 및 결과반환 후 완료 시 로그인페이지로 이동"

#로그인 페이지(폼)
@mh.route('/signin')
def signin():
    return "로그인 페이지"

#로그인 정보를 입력받아 로그인 처리
@mh.route('/signin/login', methods = ['POST'])
def signin_request():
    return "로그인 처리 및 완료 시 메인페이지로 redirect"

