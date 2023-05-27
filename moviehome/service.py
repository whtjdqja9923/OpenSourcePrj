from moviehome.repo import member
from moviehome.repo import get_member, save_member

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
