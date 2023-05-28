from flask import Blueprint, render_template, redirect
from flask_wtf import FlaskForm
from moviehome.forms import signin_form, signup_form, memberupdate_form

from moviehome.service import register, login, myinfo, update_member_info
from moviehome.repo import member

# 블루프린트 생성
mh = Blueprint('mh', __name__, url_prefix='/', template_folder="templates")

# 컨트롤러 작성

#메인페이지
@mh.route('/')
def index():
    m_id = ""
    if('member_id' in session):
        m_id = session['member_id']
        
    return render_template("index.html", member_id=m_id)

#회원가입 페이지(폼)
@mh.route('/signup', methods = ['GET', 'POST'])
def signup():
    if('member_id' in session):
        return redirect('/')
    
    form = signup_form()

    if form.validate_on_submit():
        m = member()
        m.member_id = form.data.get('member_id')
        m.password = form.data.get('password')
        password_confirm = form.data.get('password_confirm')
        m.gender = form.data.get('gender')
        m.email = form.data.get('email')
        m.age = form.data.get('age')

        result = register(m, password_confirm)
        if(result['flag']):
            return redirect('/signin')
        else:
            return render_template('register.html', form=form, error_msg=result['msg'])

    return render_template('register.html', form=form)

#로그인 페이지(폼)
@mh.route('/signin', methods = ['GET', 'POST'])
def signin():
    if('member_id' in session):
        return redirect('/')

    form = signin_form()

    if form.validate_on_submit():
        m = member()
        m.member_id = form.data.get('member_id')
        m.password = form.data.get('password')

        result = login(m)
        if(result['flag']):
            session['member_id'] = m.member_id
            return redirect('/')
        else:
            return render_template('login.html', form=form, error_msg=result['msg'])

    return render_template('login.html', form=form)

#로그아웃
@mh.route('/logout', methods = ['GET'])
def logout():
    session.clear()
    return redirect('/')

#나의정보
@mh.route('/member', methods = ['GET'])
def mypage():
    if(not 'member_id' in session):
        return redirect('/')
    
    return redirect('/member/info')

@mh.route('/member/info', methods = ['GET', 'POST'])
def member_info():
    if(not 'member_id' in session):
        return redirect('/')
    
    m = member()
    m.member_id = session['member_id']
    m = myinfo(m)
    if(not m):
        return redirect("/")
    
    form = memberupdate_form(gender=m.gender, email=m.email, age=m.age)
    
    if form.validate_on_submit():
        m.password = form.data.get('password')
        m.gender = form.data.get('gender')
        m.email = form.data.get('email')
        m.age = form.data.get('age')

        update_member_info(m)
    
    return render_template('mypage_info.html', member = m, form=form, member_id = session['member_id'])
