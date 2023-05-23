from dataclasses import dataclass, field
import sqlite3

db_path = "./share/"
db_name = "movie_data.db"

#데이터 예시
#{"movieCd":"20211567","movieNm":"수프와 이데올로기","movieNmEn":"Soup and Ideology",
# "prdtYear":"2021","openDt":"20221020","typeNm":"장편","prdtStatNm":"개봉","nationAlt":"한국",
# "genreAlt":"다큐멘터리","repNationNm":"한국","repGenreNm":"다큐멘터리",
# "directors":[{"peopleNm":"양영희"}],
# "companys":[{"companyCd":"20229503","companyNm":"㈜PLACE TO BE"},
# {"companyCd":"20229504","companyNm":"㈜나비온에어"}]}

@dataclass
class directors:
    people_name: str = ''

@dataclass
class companys:
    company_code: str = ''
    company_name: str = ''

@dataclass
class movie_data:
    movie_code: str = ''
    movie_name: str = ''
    movie_name_eng: str = ''
    prdt_year: str = ''
    open_date: str = ''
    type_name: str = ''
    prdt_stat_name: str = ''
    rep_nation_name: str = ''
    rep_genre_name: str = ''
    directors: list[directors] = field(default_factory=list)
    companys: list[companys] = field(default_factory=list)

#데이터 예시
# {"peopleCd":"20389164","peopleNm":"리아드 벨라이체",
# "peopleNmEn":"Riadh Belaiche","repRoleNm":"배우","filmoNames":""}

@dataclass
class people_data:
    people_code: str = ''
    poeple_name: str = ''
    people_name_eng: str = ''
    rep_role_name: str = ''
    filmo_names: list[str] = field(default_factory=list)

#테이블 조회 후 없으면 필요테이블 생성
def create_table_movie():
    con = sqlite3.connect(db_path + db_name)
    cursor = con.cursor()

    ddl_movie_basic = ''' CREATE TABLE movie_basic ( 
        "movie code"         VARCHAR(255) NOT NULL  PRIMARY KEY  ,
        "movie name"         VARCHAR(255) NOT NULL    ,
        "movie name eng"     VARCHAR(255)     ,
        "prdt year"          VARCHAR(4)     ,
        "open date"          VARCHAR(8) NOT NULL    ,
        "type name"          VARCHAR(255)     ,
        "prdt stat name"     VARCHAR(255)     ,
        "rep nation name"    VARCHAR(255) NOT NULL    ,
        "rep genre name"     VARCHAR(255) NOT NULL    
        ); '''
    ddl_companys = ''' CREATE TABLE companys ( 
        "movie code"         VARCHAR(255) NOT NULL    ,
        "company code"       VARCHAR(255) NOT NULL    ,
        "company name"       VARCHAR(255)     ,
        CONSTRAINT pk2 PRIMARY KEY ( "movie code", "company code" ),
        FOREIGN KEY ( "movie code" ) REFERENCES movie_basic( "movie code" )  
        ); '''
    ddl_directors = ''' CREATE TABLE directors ( 
        "director num"       INTEGER NOT NULL  PRIMARY KEY  ,
        "movie code"         VARCHAR(255) NOT NULL    ,
        "people name"        VARCHAR(255)     ,
        FOREIGN KEY ( "movie code" ) REFERENCES movie_basic( "movie code" )  
        ); '''
    ddl_people_basic = ''' CREATE TABLE people_basic ( 
        "people code"        VARCHAR(255) NOT NULL  PRIMARY KEY  ,
        "people name"        VARCHAR(255) NOT NULL    ,
        "people name eng"    VARCHAR(255)     ,
        "rep role name"      VARCHAR(255) NOT NULL  
        ); '''
    ddl_people_filmo = ''' CREATE TABLE people_filmo ( 
        "filmo num"          INTEGER NOT NULL  PRIMARY KEY  ,
        "people code"        VARCHAR(255) NOT NULL    ,
        "filmo name"         VARCHAR(255) NOT NULL    ,
        FOREIGN KEY ( "people code" ) REFERENCES people_basic( "people code" )  
        ); '''
        
    if not cursor.execute('''select name from sqlite_master where type="table" and name="movie_basic"''').fetchall():
        cursor.execute(ddl_movie_basic)
    if not cursor.execute('''select name from sqlite_master where type="table" and name="companys"''').fetchall():
        cursor.execute(ddl_companys)
    if not cursor.execute('''select name from sqlite_master where type="table" and name="directors"''').fetchall():
        cursor.execute(ddl_directors)
    if not cursor.execute('''select name from sqlite_master where type="table" and name="people_basic"''').fetchall():
        cursor.execute(ddl_people_basic)
    if not cursor.execute('''select name from sqlite_master where type="table" and name="people_filmo"''').fetchall():
        cursor.execute(ddl_people_filmo)

    con.commit()

    cursor.close()
    con.close()

def save_movie_list(data:movie_data):
    con = sqlite3.connect(db_path + db_name)
    cursor = con.cursor()

    insert_movie_basic = '''
        INSERT INTO movie_basic ( 
            "movie code", "movie name", "movie name eng", "prdt year", 
            "open date", "type name", "prdt stat name", "rep nation name", 
            "rep genre name" ) 
            VALUES ( ?, ?, ?, ?, ?, ?, ?, ?, ? )
    '''
    movie_data = [data.movie_code, data.movie_name, data.movie_name_eng, 
                   data.prdt_year, data.open_date, data.type_name, 
                   data.prdt_stat_name, data.rep_nation_name, data.rep_genre_name]
    try:
        cursor.execute(insert_movie_basic, movie_data)
    except:
        pass

    for company in data.companys:
        insert_companys = '''
            INSERT INTO companys ( 
                "movie code", "company code", "company name" ) 
                VALUES ( ?, ?, ? )
        '''
        company_data = [data.movie_code, company.company_code, company.company_name]

        try:
            cursor.execute(insert_companys, company_data)
        except:
            pass

    for director in data.directors:
        insert_companys = '''
            INSERT INTO directors (
                "movie code", "people name" )
                VALUES ( ?, ? )
        '''
        director_data = [data.movie_code, director.people_name]

        try:
            cursor.execute(insert_companys, director_data)
        except:
            pass
        
    con.commit()
    cursor.close()
    con.close()