from dataclasses import dataclass, field
import sqlite3

@dataclass(frozen=True)
class path:
    db_path = "./share/"
    db_name = "user_data.db"

@dataclass
class member:
    member_code: str = ""
    member_id: str = ""
    password: str = ""
    gender: str = ""
    email: str = ""
    age: str = ""

def create_table_movie():
    con = sqlite3.connect(path.db_path + path.db_name)
    cursor = con.cursor()

    ddl_member = ''' CREATE TABLE member ( 
        "member code"        INTEGER NOT NULL  PRIMARY KEY  ,
        "member id"          VARCHAR(255) NOT NULL  UNIQUE  ,
        password             VARCHAR(255) NOT NULL    ,
        gender               VARCHAR(255)     ,
        email                VARCHAR(255)     ,
        age                  INTEGER     ,
        CONSTRAINT "unq_member_member code" UNIQUE ( "member code" )
        ); '''
    ddl_favorite = ''' CREATE TABLE favorite ( 
        "favorite id"        INTEGER NOT NULL  PRIMARY KEY  ,
        "member code"        INTEGER NOT NULL    ,
        "type"               VARCHAR(255)     ,
        "people code"        VARCHAR(255)     ,
        "movie code"         VARCHAR(255)     ,
        FOREIGN KEY ( "member code" ) REFERENCES member( "member code" )  
        ); '''
    
    if not cursor.execute('''select name from sqlite_master where type="table" and name="member"''').fetchall():
        cursor.execute(ddl_member)
    if not cursor.execute('''select name from sqlite_master where type="table" and name="favorite"''').fetchall():
        cursor.execute(ddl_favorite)

    con.commit()

    cursor.close()
    con.close()

def save_member(m:member):
    con = sqlite3.connect(path.db_path + path.db_name)
    cursor = con.cursor()

    if(not (m.member_id and m.password and m.gender and m.email and m.age)):
        return "항목 누락"

    query = ''' INSERT INTO member ( "member id", password, gender, email, age ) VALUES (?, ?, ?, ?, ?)
    '''
    data = [m.member_id, m.password, m.gender, m.email, m.age]

    cursor.execute(query, data)

    con.commit()

    cursor.close()
    con.close()

    return

def get_member(m:member, all=False):
    con = sqlite3.connect(path.db_path + path.db_name)
    cursor = con.cursor()

    query_before = ''' SELECT m."member code" as member_code, m."member id" as member_id, m.password, m.gender, m.email, m.age
    FROM member m 
    '''

    where = ""
    if all == True:
        where += ";"
    else:
        #where절 생성을 위해 입력받은 변수 확인
        where = "WHERE "
        if m.member_id != "":
            where += 'm."member id" = "' + m.member_id + '";'

    result = []
    for row in cursor.execute(query_before + where).fetchall():
        row = list(row)
        result.append(member(row[0], row[1], row[2], row[3], row[4], row[5]))

    return result

def update_member(m:member):
    con = sqlite3.connect(path.db_path + path.db_name)
    cursor = con.cursor()

    query_before = ''' UPDATE member set password = ?, gender = ?, email = ?, age = ? WHERE "member id" = ?;
    '''

    data = [m.password, m.gender, m.email, m.age, m.member_id]

    cursor.execute(query_before, data)
    
    con.commit()

    cursor.close()
    con.close()

    return

def save_favorite(m:member):
    return ""

def get_favorite():
    return ""
