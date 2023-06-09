from flask import Blueprint, render_template, redirect, session, request, make_response, flash
from flask_paginate import Pagination, get_page_args
from flask_wtf import FlaskForm
from movie_home.forms import signin_form, signup_form, memberupdate_form, search_form

from movie_home.service import register, login, myinfo, update_member_info, movie_list, user_rating, actor_list
from movie_home.repo import member

# 블루프린트 생성
mh = Blueprint('mh', __name__, url_prefix='/')

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

@mh.route('/member/myMovie', methods = ['GET'])
def member_my_movie():
    if(not 'member_id' in session):
        return redirect('/')
    
    return render_template('mypage_movie.html', member_id = session['member_id'])

@mh.route('/member/myFavorite', methods = ['GET'])
def member_my_favorite():
    if(not 'member_id' in session):
        return redirect('/')
    
    return render_template('mypage_favorite.html', member_id = session['member_id'])

@mh.route('/movies', methods = ['GET', 'POST'])
def main_movie_list():
    #로그인여부 체크
    m_id = ""
    if('member_id' in session):
        m_id = session['member_id']
    else:
        flash("로그인이 필요한 서비스입니다.")
        return redirect('/signin')
        
    per_page = 3
    page, _, offset = get_page_args(per_page=per_page)
        
    form = search_form()
    if form.validate_on_submit():
        keyword = form.data.get('search')
        model, total = movie_list(keyword = keyword, m_id=m_id, col_num = 3, per_page = per_page, offset = offset)
    else:
        model, total = movie_list(m_id=m_id, col_num = 3, per_page = per_page, offset = offset)
        
    return render_template("movie_list.html", member_id=m_id, movie_list=model, form=form, 
                           pagination = Pagination(
                               page = page,
                               total = total,
                               per_page = per_page,
                               prev_label = '<<',
                               next_label = '>>',
                               format_total = True
                           ))

@mh.route('/actors', methods = ['GET', 'POST'])
def main_actor_list():
    #로그인여부 체크
    m_id = ""
    if('member_id' in session):
        m_id = session['member_id']
    else:
        flash("로그인이 필요한 서비스입니다.")
        return redirect('/signin')
        
    per_page = 50
    page, _, offset = get_page_args(per_page=per_page)
        
    form = search_form()
    if form.validate_on_submit():
        keyword = form.data.get('search')
        model, total = actor_list(keyword = keyword, m_id=m_id, col_num = 3, per_page = per_page, offset = offset)
    else:
        model, total = actor_list(m_id=m_id, col_num = 3, per_page = per_page, offset = offset)
        
    return render_template("actor_list.html", member_id=m_id, people_list=model, form=form, 
                           pagination = Pagination(
                               page = page,
                               total = total,
                               per_page = per_page,
                               prev_label = '<<',
                               next_label = '>>',
                               format_total = True
                           ))

@mh.route('/user/rating', methods = ['POST'])
def rating():
    #로그인여부 체크
    m_id = ""
    if('member_id' in session):
        m_id = session['member_id']
    else:
        flash("로그인이 필요한 서비스입니다.")
        return redirect('/signin')
        
    if(not m_id):
        return make_response("success", 200)
    
    params = request.get_json()
    params['member_id'] = m_id
    
    user_rating(params, type=params['type'])
    
    return make_response("success", 200)
