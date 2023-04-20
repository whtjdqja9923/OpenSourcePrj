import pymysql

"""
<테이블 네이밍>
:movie_classification: 영화 분류기준 정보를 모아놓은 테이블(genres 등)
:movies: 모든 영화정보 목록을 모아놓은 테이블
:genre(horror, romance 등): 장르 별 영화정보들을 모아놓은 테이블
:ratings: 평점과 id를 매칭시켜 모아놓은 테이블
:actor: 배우별로 출연한 영화id와 평점을 모아놓은 테이블
"""

"""
<계획에 따라 작성할 수도 있는 함수>
:get_top_n_title_by_actor: actor를 입력받아 해당 actor가 출연한 영화 title rating 순으로 n만큼 반환
"""





# id를 입력하면 해당 id의 title을 반환
def get_title_by_id(movie_id):
     # DB 연결
    connection = pymysql.connect(
        host="localhost",
        user="username",
        password="password",
        db="database_name",
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor
        )

    # 해당 id의 title을 반환
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM title WHERE id=%s"
            cursor.execute(sql, movie_id)
            result = cursor.fetchone()
            return result['title']
    # 예외 처리
    except Exception as e:
        print(f"Error: {e}")
    # DB 연결
    finally:
        connection.close()





# id를 입력하면 해당 id의 rating을 반환
def get_rating_by_id(movie_id):
    # DB 연결
    connection = pymysql.connect(
        host="localhost",
        user="username",
        password="password",
        db="database_name",
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor
        )

    # 해당 id의 rating을 반환
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM ratings WHERE id=%s"
            cursor.execute(sql, movie_id)
            result = cursor.fetchone()
            return result['rating']
    # 예외 처리
    except Exception as e:
        print(f"Error: {e}")
    # DB 연결
    finally:
        connection.close()





# id를 입력하면 해당 id의 actor를 n만큼 반환
def get_n_actors_by_id(movie_id, n):
    # DB 연결
    connection = pymysql.connect(
        host="localhost",
        user="username",
        password="password",
        db="database_name",
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor
        )

    # 해당 id의 actor를 n만큼 반환
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM movies WHERE id=%s"
            cursor.execute(sql, movie_id)
            result = cursor.fetchmany(n)
            return [r['actor'] for r in result]
    # 예외 처리
    except Exception as e:
        print(f"Error: {e}")
    # DB 연결
    finally:
        connection.close()





# id, n을 입력하면 해당 id의 genres를 n개 만큼 리스트로 반환
def get_n_genres_by_id(movie_id, n):
    # DB 연결
    connection = pymysql.connect(
        host="localhost",
        user="username",
        password="password",
        db="database_name",
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor
        )

    # 해당 영화의 genre를 n만큼 list로 반환
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM movies WHERE movie_id=movie_id LIMIT %s"
            cursor.execute(sql, n)
            result = cursor.fetchmany(n)
            return [r['genre'] for r in result]
    # 예외 처리
    except Exception as e:
        print(f"Error: {e}")
    # DB 연결 종료
    finally:
        connection.close()





# rating이 가장 높은 n개의 영화정보 반환
def get_top_n_movies(n):
    # DB 연결
    connection = pymysql.connect(
        host="localhost",
        user="username",
        password="password",
        db="database_name",
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor
        )

    # 해당 genre의 title을 count만큼 list로 반환
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM genre ORDER BY rating LIMIT %s"
            cursor.execute(sql, n)
            result = cursor.fetchmany(n)
            return [r['title'] for r in result]
    # 예외 처리
    except Exception as e:
        print(f"Error: {e}")
    # DB 연결 종료
    finally:
        connection.close()


        


# 해당 genre의 rating이 가장 높은 n개의 영화정보 반환
def get_top_n_movies_by_genre(genre, n):
    # DB 연결
    connection = pymysql.connect(
        host="localhost",
        user="username",
        password="password",
        db="database_name",
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor
        )

    # 해당 genre의 title을 count만큼 list로 반환
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM genre ORDER BY rating LIMIT %s"
            cursor.execute(sql, (genre, n))
            result = cursor.fetchmany(n)
            return [r['title'] for r in result]
    # 예외 처리
    except Exception as e:
        print(f"Error: {e}")
    # DB 연결 종료
    finally:
        connection.close()





# 모든 장르를 list로 반환
def get_genres():
    # DB 연결
    connection = pymysql.connect(
        host="localhost",
        user="username",
        password="password",
        db="database_name",
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor
        )

    # 해당 genre의 title을 count만큼 list로 반환
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM movie_classification WHERE id=%s"
            cursor.execute(sql, ('genres'))
            result = cursor.fetchall()
            return [r['genre'] for r in result]
    # 예외 처리
    except Exception as e:
        print(f"Error: {e}")
    # DB 연결 종료
    finally:
        connection.close()





# 추천 영화목록 반환
def get_movie_recommendation_list():
    list = {"a", "b", "c"}

    return list