from movie_home.repo import member
from movie_home.repo import get_member, save_member
import movie_crawler as mv

def login(m:member):
    compare = get_member(m)
    result = {"flag":True, "msg":""}

    #아이디가 존재하지 않거나 비밀번호가 맞지 않으면
    if (not compare):
        result["flag"] = False
        result["msg"] = "아이디가 존재하지 않습니다"
    elif m.password != compare[0].password:
        result["flag"] = False
        result["msg"] = "비밀번호가 일치하지 않습니다"
    
    return result

def register(m:member, password_confirm):
    result = {"flag":False, "msg":"등록에 실패하였습니다"}

    if get_member(m):
        result['msg'] = '동일한 아이디가 존재합니다'
    elif (m and (m.password == password_confirm)):
        result["flag"] = True
        result["msg"] = "등록성공!"
        save_member(m)

    return result

#member id를 활용해 member 정보 조회
def myinfo(m:member):
    result = get_member(m)

    if (not result) or (len(result) > 1):
        return "" # 공백 반환

    return result[0]

def update_member_info(m:member):
    result = {"flag":False, "msg":"변경에 실패하였습니다"}
    
    try:
        update_member(m)
        result["flag"] = True
        result["msg"] = "변경성공!"
    except:
        return result

    return result

def movie_list(col_num=3, keyword="", m_id="", per_page=12, offset=0):
    m_code = "None"
    if m_id:
        mem = get_member(member(member_id=m_id))
        m_code = mem[0].member_code
    
    if not keyword:
        movies = mv.get_movie_list_audience_desc(m_code)
    else:
        basic = mv.get_movie(movie_name=keyword)
        rating = []
        user_rating = []
        
        user = mv.get_rating(code=m_code, type="member")
        for i in range(len(basic)):
            rating.append((mv.get_rating(code=basic[i].movie_code, type="movie")[0]))
            for j in range(len(user)):
                flag = False
                if basic[i].movie_code == user[j].movie_code:
                    user_rating.append(user[j])
                    flag = True
                    break
            if not flag:
                user_rating.append(mv.movie_rating())
            
        movies = list(zip(basic, rating, user_rating))
        
    m = []
    for movie in movies:
        if movie[0].show_time:
            movie[0].show_time = (str(int(int(movie[0].show_time)/60)) + "시간 " + str(int(int(movie[0].show_time)%60))+"분")
        m.append({
            "movie_code":movie[0].movie_code,
            "movie_name":movie[0].movie_name,
            "prdt_year":movie[0].prdt_year,
            "type_name":movie[0].type_name,
            "rep_genre_name":movie[0].rep_genre_name,
            "show_time":movie[0].show_time,
            "poster_img_link":movie[0].poster_img_link,
            "audience_num":movie[0].audience_num,
            "score":movie[1].score,
            "max_score":movie[1].max_score,
            "source":movie[1].source,
            "rating_count":movie[1].rating_count,
            "user_rating":movie[2].score,
            "user_max_rating":movie[2].max_score
        })
        
    if keyword:
        m = sorted(m, key=(lambda x : int(x['audience_num']) if x['audience_num'] is not None else 0), reverse=True)    
    result = []
    for i in range(0, len(m), col_num):
        result.append(m[i:i+col_num])
        
    return result[offset:offset+per_page], len(result)

def user_rating(data:dict={}, type="movie"):
    d = mv.movie_rating()
    d.type = type
    d.source = "user"
    d.score = data["score"]
    d.max_score = data["max_score"]
    
    m = get_member(member(member_id=data["member_id"]))
    d.member_code = m[0].member_code
    if type == "movie":
        d.movie_code = data["movie_code"]
        d.people_code = ""
    elif type == "people":
        d.people_code = data["people_code"]
        d.movie_code = ""
    
    before = mv.get_rating(code=d.member_code, type="member")
    if type == "movie":
        if before is not None and any(item.movie_code == data['movie_code'] for item in before):
            mv.save_rating(d, type="update")
        else:
            mv.save_rating(d, type="insert")
    elif type == "people":
        if before is not None and any(item.people_code == data['people_code'] for item in before):
            mv.save_rating(d, type="update")
        else:
            mv.save_rating(d, type="insert")

def actor_list(col_num=3, keyword="", m_id="", per_page=12, offset=0):
    m_code = "None"
    if m_id:
        mem = get_member(member(member_id=m_id))
        m_code = mem[0].member_code
    
    if not keyword:
        basic = mv.get_people(all=True, off_set=offset, per_page=per_page)
        l = len(mv.get_people(all=True, off_set=0, per_page=100000000))
    else:
        basic = mv.get_people(people_name=keyword, off_set=offset, per_page=per_page)
        l = len(mv.get_people(people_name=keyword, off_set=0, per_page=100000000))
        
    rating = []
    user_rating = []
    
    user = mv.get_rating(code=m_code, type="member")
    for i in range(len(basic)):
        rating.append((mv.get_rating(code=basic[i].people_code, type="people")[0] if
                      mv.get_rating(code=basic[i].people_code, type="people") else mv.movie_rating()))
        for j in range(len(user)):
            flag = False
            if basic[i].people_code == user[j].people_code:
                user_rating.append(user[j])
                flag = True
                break
        if not flag:
            user_rating.append(mv.movie_rating())
        
    peoples = list(zip(basic, rating, user_rating))
        
    p = []
    for people in peoples:
        filmo_compact = people[0].filmo_compact.split('|')
        p.append({
            "people_code":people[0].people_code,
            "people_name":people[0].people_name,
            "rep_role_name":people[0].rep_role_name,
            "filmo_compact":filmo_compact[:5],
            "score":people[1].score,
            "max_score":people[1].max_score,
            "source":people[1].source,
            "rating_count":people[1].rating_count,
            "user_rating":people[2].score,
            "user_max_rating":people[2].max_score
        })
        
    p = sorted(p, key=(lambda x : x['people_name'] if x['people_name'] is not None else ""), reverse=False)
        
    return p, l
