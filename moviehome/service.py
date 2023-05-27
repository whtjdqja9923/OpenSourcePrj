from moviehome.repo import member
from moviehome.repo import get_member, save_member

def register(m:member, password_confirm):
    result = {"flag":False, "msg":"등록에 실패하였습니다"}

    if get_member(m):
        result['msg'] = '동일한 아이디가 존재합니다'
    elif (m and (m.password == password_confirm)):
        result["flag"] = True
        result["msg"] = "등록성공!"
        save_member(m)

    return result
