from dataclasses import dataclass, field
import sqlite3

db_path = "./share/"
db_name = "database.db"

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
    movie_name_org: str = ''
    show_time: str = ''
    poster_img_link: str = ''
    synopsis: str = ''
    audience_num: str = ''
    directors: list[directors] = field(default_factory=list)
    companys: list[companys] = field(default_factory=list)

@dataclass
class movie_rating:
    rating_id: str = ''
    movie_code: str = ''
    member_code: str = ''
    people_code: str = ''
    type: str = ''
    score: str = ''
    max_score: str = ''
    rating_count: str = ''
    source: str = ''

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
    filmo_comapct: str = ''

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
        "rep genre name"     VARCHAR(255) NOT NULL    ,
        "poster img link"    VARCHAR(1000)     
        ); '''
    ddl_companys = ''' CREATE TABLE companys ( 
        "movie code"         VARCHAR(255) NOT NULL    ,
        "company code"       VARCHAR(255) NOT NULL    ,
        "company name"       VARCHAR(255)     ,
        CONSTRAINT pk2 PRIMARY KEY ( "movie code", "company code" ),
        FOREIGN KEY ( "movie code" ) REFERENCES movie_basic( "movie code" ) ON DELETE CASCADE 
        ); '''
    ddl_directors = ''' CREATE TABLE directors ( 
        "director num"       INTEGER NOT NULL  PRIMARY KEY  ,
        "movie code"         VARCHAR(255) NOT NULL    ,
        "people name"        VARCHAR(255)     ,
        FOREIGN KEY ( "movie code" ) REFERENCES movie_basic( "movie code" ) ON DELETE CASCADE 
        ); '''
    ddl_people_basic = ''' CREATE TABLE people_basic ( 
	    "people code"        VARCHAR(255) NOT NULL  PRIMARY KEY  ,
	    "people name"        VARCHAR(255) NOT NULL    ,
	    "people name eng"    VARCHAR(255)     ,
	    "rep role name"      VARCHAR(255)     ,
	    "filmo compact"      VARCHAR(1000)     
        ); '''
    ddl_people_filmo = ''' CREATE TABLE people_filmo ( 
        "filmo num"          INTEGER NOT NULL  PRIMARY KEY  ,
        "people code"        VARCHAR(255) NOT NULL    ,
        "filmo name"         VARCHAR(255) NOT NULL    ,
        FOREIGN KEY ( "people code" ) REFERENCES people_basic( "people code" ) ON DELETE CASCADE 
        ); '''
    ddl_movie_detail = ''' CREATE TABLE movie_detail ( 
        "movie code"         VARCHAR(255) NOT NULL  PRIMARY KEY  ,
        "movie name org"     VARCHAR(255)     ,
        "show time"          VARCHAR(255) NOT NULL    ,
        synopsis             VARCHAR(1000)     ,
        "audience num"       VARCHAR(255)     ,
        FOREIGN KEY ( "movie code" ) REFERENCES movie_basic( "movie code" )  
        ); '''
    ddl_rating = ''' CREATE TABLE rating ( 
        "rating id"          INTEGER NOT NULL  PRIMARY KEY  ,
        "type"               VARCHAR(255) NOT NULL    ,
        score                VARCHAR(255)     ,
        "max score"          VARCHAR(255)     ,
        "rating count"       VARCHAR(255)     ,
        source               VARCHAR(255)     ,
        "movie code"         VARCHAR(255)     ,
        "people code"        VARCHAR(255)     ,
        "member code"        INTEGER     ,
        FOREIGN KEY ( "movie code" ) REFERENCES movie_basic( "movie code" ) ON DELETE CASCADE  ,
        FOREIGN KEY ( "people code" ) REFERENCES people_basic( "people code" ) ON DELETE CASCADE  ,
        FOREIGN KEY ( "member code" ) REFERENCES member( "member code" ) ON DELETE CASCADE  
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
    if not cursor.execute('''select name from sqlite_master where type="table" and name="movie_detail"''').fetchall():
        cursor.execute(ddl_movie_detail)
    if not cursor.execute('''select name from sqlite_master where type="table" and name="rating"''').fetchall():
        cursor.execute(ddl_rating)

    con.commit()

    cursor.close()
    con.close()

def save_movie_list(data_list:list[movie_data]):
    con = sqlite3.connect(db_path + db_name)
    cursor = con.cursor()

    insert_movie_basic = '''
        INSERT INTO movie_basic ( 
            "movie code", "movie name", "movie name eng", "prdt year", 
            "open date", "type name", "prdt stat name", "rep nation name", 
            "rep genre name" ) 
            VALUES ( ?, ?, ?, ?, ?, ?, ?, ?, ? )
    '''
    insert_companys = '''
            INSERT INTO companys ( 
                "movie code", "company code", "company name" ) 
                VALUES ( ?, ?, ? )
    '''
    insert_directors = '''
            INSERT INTO directors (
                "movie code", "people name" )
                VALUES ( ?, ? )
    '''

    movie_data = []
    company_data = []
    director_data = []
    for data in data_list:
        movie_data.append([data.movie_code, data.movie_name, data.movie_name_eng, 
                            data.prdt_year, data.open_date, data.type_name, 
                            data.prdt_stat_name, data.rep_nation_name, data.rep_genre_name])
        
        for company in data.companys:
            company_data.append([data.movie_code, company.company_code, company.company_name])

        for director in data.directors:
            director_data.append([data.movie_code, director.people_name])

    
    cursor.executemany(insert_movie_basic, movie_data)
    cursor.executemany(insert_companys, company_data)
    cursor.executemany(insert_directors, director_data)
        
    con.commit()
    cursor.close()
    con.close()

def save_people_list(data_list:list[people_data]):
    con = sqlite3.connect(db_path + db_name)
    cursor = con.cursor()
    
    insert_people_basic = '''
        INSERT INTO people_basic ( 
            "people code", "people name", "people name eng", "rep role name", "filmo compact" ) 
            VALUES ( ?, ?, ?, ?, ? )
    '''
    insert_filmo_names = '''
        INSERT INTO people_filmo ( 
            "people code", "filmo name" ) 
            VALUES ( ?, ? )
    '''
    people_data = []
    filmo_data = []
    for data in data_list:
        people_data.append([data.people_code, data.poeple_name, data.people_name_eng, data.rep_role_name, data.filmo_comapct])

        for filmo_name in data.filmo_names:
            filmo_data.append([data.people_code, filmo_name])

    cursor.executemany(insert_people_basic, people_data)
    cursor.executemany(insert_filmo_names, filmo_data)

    con.commit()
    cursor.close()
    con.close()

def save_movie_basic(data:movie_data):
    con = sqlite3.connect(db_path + db_name)
    cursor = con.cursor()

    upsert_movie_basic = '''
        INSERT INTO movie_basic ( 
            "movie code", "movie name", "movie name eng", "prdt year", 
            "open date", "type name", "prdt stat name", "rep nation name", 
            "rep genre name", "poster img link" ) 
            VALUES ( ?, ?, ?, ?, ?, ?, ?, ?, ?, ? )
        ON CONFLICT ("movie code") DO UPDATE
        SET "movie name" = ?, "movie name eng" = ?, "prdt year" = ?, 
            "open date" = ?, "type name" = ?, "prdt stat name" = ?, "rep nation name" = ?, 
            "rep genre name" = ?, "poster img link" = ?
        WHERE "movie code" = ?
        '''
    
    movie_data = [data.movie_code, data.movie_name, data.movie_name_eng, data.prdt_year, data.open_date, 
                    data.type_name, data.prdt_stat_name, data.rep_nation_name, data.rep_genre_name, data.poster_img_link,
                    data.movie_name, data.movie_name_eng, data.prdt_year, data.open_date, data.type_name, 
                    data.prdt_stat_name, data.rep_nation_name, data.rep_genre_name, data.poster_img_link, data.movie_code]

    
    cursor.execute(upsert_movie_basic, movie_data)
        
    con.commit()
    cursor.close()
    con.close()    

def save_movie_detail(data:movie_data):
    con = sqlite3.connect(db_path + db_name)
    cursor = con.cursor()
    
    upsert_movie_detail = '''
        INSERT INTO movie_detail ( 
            "movie code", "movie name org", "show time", synopsis, "audience num" ) 
            VALUES ( ?, ?, ?, ?, ? )
        ON CONFLICT ("movie code") DO UPDATE 
        SET "movie name org" = ?, "show time" = ?, synopsis = ?, "audience num" = ?
        WHERE "movie code" = ?
    '''

    movie_data = [data.movie_code, data.movie_name_org, data.show_time, data.synopsis, data.audience_num,
                  data.movie_name_org, data.show_time, data.synopsis, data.audience_num, data.movie_code]

    cursor.execute(upsert_movie_detail, movie_data)

    con.commit()
    cursor.close()
    con.close()

def save_rating(data:movie_rating, type="insert"):
    con = sqlite3.connect(db_path + db_name)
    cursor = con.cursor()
    
    upsert_rating = '''
        INSERT INTO rating (
            "rating id", "type", "score", "max score", "rating count", "source", "movie code", "people code", "member code" )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT ( "rating id" ) DO UPDATE
        SET "type" = ?, "score" = ?, "max score" = ?, "rating count" = ?, "source" = ?, "movie code" = ?, "people code" = ?, "member code"  = ?
        WHERE "rating id" = ?
    '''
    insert_rating = '''
        INSERT INTO rating (
            "type", "score", "max score", "rating count", "source", "movie code", "people code", "member code" )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    '''

    if type == 'insert':
        rating_data = [data.type, data.score, data.max_score, data.rating_count, data.score, data.movie_code, data.people_code, data.member_code]
        cursor.execute(insert_rating, rating_data)
    elif type == 'upsert':
        rating_data = [data.rating_id, data.type, data.score, data.max_score, data.rating_count, data.score, data.movie_code, data.people_code, data.member_code,
                       data.type, data.score, data.max_score, data.rating_count, data.score, data.movie_code, data.people_code, data.member_code, data.rating_id]
        cursor.execute(upsert_rating, rating_data)

    con.commit()
    cursor.close()
    con.close()

#영화 검색
def get_movie(all=False, movie_code = "", movie_name = "", movie_name_eng = "", prdt_year = "", 
              open_date = "", type_name = "", prdt_stat_name = "", rep_nation_name = "", rep_genre_name = "", movie_name_org = "", synopsis = "")->list:
    
    con = sqlite3.connect(db_path + db_name)
    con.row_factory = sqlite3.Row
    cursor = con.cursor()

    query_before = ''' SELECT mb."movie code" as movie_code, mb."movie name" as movie_name, mb."movie name eng" as movie_name_eng, 
        mb."prdt year" as prdt_year, mb."open date" as open_date, mb."type name" as type_name, mb."prdt stat name" as prdt_stat_name, mb."rep nation name" as rep_nation_name, 
        mb."rep genre name" as rep_genre_name, md."movie name org" as movie_name_org, md."show time" as show_time, mb."poster img link" as poster_img_link, md.synopsis, md."audience num" as audience_num
        FROM movie_basic mb 
	    LEFT OUTER JOIN movie_detail md ON ( md."movie code" = mb."movie code"  )
    '''

    if all == True:
        where += ";"
    else:
        #where절 생성을 위해 입력받은 변수 확인
        where = "WHERE "
        if movie_code != "":
            where += 'mb."movie code" LIKE "%' + movie_code + '%" AND '
        if movie_name != "":
            where += 'mb."movie name" LIKE "%' + movie_name + '%" AND '
        if movie_name_eng != "":
            where += 'mb."movie name eng" LIKE "%' + movie_name_eng + '%" AND '
        if prdt_year != "":
            where += 'mb."prdt year" = "' + prdt_year + '" AND '
        if open_date != "":
            where += 'mb."open date" = "' + open_date + '" AND '
        if type_name != "":
            where += 'mb."type name" LIKE "%' + type_name + '%" AND '
        if prdt_stat_name != "":
            where += 'mb."prdt stat name" = "' + prdt_stat_name + '" AND '
        if rep_nation_name != "":
            where += 'mb."rep nation name" = "' + rep_nation_name + '" AND '
        if rep_genre_name != "":
            where += 'mb."rep genre name" LIKE "%' + rep_genre_name + '%" AND '    
        if movie_name_org != "":
            where += 'md."movie name org" LIKE "%' + movie_name_org + '%" AND '
        if synopsis != "":
            where += 'md.synopsis LIKE "%' + synopsis + '%" AND '     
        #끝에 AND 제거
        if where != "":
            where = where[:-5]
            where += ";"

    result = []
    for row in cursor.execute(query_before + where).fetchall():
        row = list(row)
        result.append(movie_data(row[0], row[1], row[2], row[3], row[4], row[5], row[6], 
                                 row[7], row[8], row[9], row[10], row[11], row[12], row[13]))

    cursor.close()
    con.close()

    return result

def get_people(all=False, people_code="", people_name="", people_name_eng="", rep_role_name="", filmo_compact=""):
    con = sqlite3.connect(db_path + db_name)
    con.row_factory = sqlite3.Row
    cursor = con.cursor()

    query_before = ''' SELECT pb."people code" as people_code, pb."people name" as people_name, pb."people name eng" as people_name_eng, pb."filmo compact" as filmo_compact
    pb."rep role name" as rep_role_name
        FROM people_basic pb 
    '''

    if all == True:
        where += ";"
    else:
        #where절 생성을 위해 입력받은 변수 확인
        where = "WHERE "
        if people_code != "":
            where += 'pb."people code" LIKE "%' + people_code + '%" AND '
        if people_name != "":
            where += 'pb."people name" LIKE "%' + people_name + '%" AND '
        if people_name_eng != "":
            where += 'pb."people name eng" LIKE "%' + people_name_eng + '%" AND '
        if rep_role_name != "":
            where += 'pb."rep role name" LIKE "%' + rep_role_name + '%" AND '
        if filmo_compact != "":
            where += 'pb."filmo compact" LIKE "%' + filmo_compact + '%" AND '
        #끝에 AND 제거
        if where != "":
            where = where[:-5]
            where += ";"

    result = []
    for row in cursor.execute(query_before + where).fetchall():
        row = list(row)
        result.append(people_data(row[0], row[1], row[2], row[3], row[4]))

    cursor.close()
    con.close()

    return result

def get_filmo(all=False, people_code="", filmo_name=""):
    con = sqlite3.connect(db_path + db_name)
    con.row_factory = sqlite3.Row
    cursor = con.cursor()

    query_before = ''' SELECT pf."people code" as people_code, pf."filmo name" as filmo_name, pb."people name" as people_name, pb."people name eng" as people_name_eng, pb."rep role name" as rep_role_name
    FROM people_filmo pf 
	RIGHT OUTER JOIN people_basic pb ON ( pb."people code" = pf."people code"  )  
    '''

    if all == True:
        where += ";"
    else:
        #where절 생성을 위해 입력받은 변수 확인
        where = "WHERE "
        if people_code != "":
            where += 'pf."people code" LIKE "%' + people_code + '%" AND '
        if filmo_name != "":
            where += 'pf."filmo name" LIKE "%' + filmo_name + '%" AND '
        if where != "":
            where = where[:-5]
            where += ";"

    result = []
    for row in cursor.execute(query_before + where).fetchall():
        result.append(dict(row))

    cursor.close()
    con.close()

    return result