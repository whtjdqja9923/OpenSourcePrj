import pymysql

"""
<���̺� ���̹�>
:movie_classification: ��ȭ �з����� ������ ��Ƴ��� ���̺�(ex. genres: ȣ��, �θǽ�, �׼�)
:movies: ��� ��ȭ���� ����� ��Ƴ��� ���̺�(rating, id, genre ��)
:genre(horror, romance ��): �帣 �� �ش� ��ȭ�������� ��Ƴ��� ���̺�
:ratings: ������ id�� ��Ī���� ��Ƴ��� ���̺�
"""





# id�� �Է��ϸ� �ش� id�� title�� ��ȯ
def get_title_by_id(movie_id):
     # DB ����
    connection = pymysql.connect(
        host="localhost",
        user="username",
        password="password",
        db="database_name",
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor
        )

    # �ش� id�� title�� ��ȯ
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM title WHERE id=%s"
            cursor.execute(sql, movie_id)
            result = cursor.fetchone()
            return result['title']
    # ���� ó��
    except Exception as e:
        print(f"Error: {e}")
    # DB ����
    finally:
        connection.close()





# id�� �Է��ϸ� �ش� id�� rating�� ��ȯ
def get_rating_by_id(movie_id):
    # DB ����
    connection = pymysql.connect(
        host="localhost",
        user="username",
        password="password",
        db="database_name",
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor
        )

    # �ش� id�� rating�� ��ȯ
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM ratings WHERE id=%s"
            cursor.execute(sql, movie_id)
            result = cursor.fetchone()
            return result['rating']
    # ���� ó��
    except Exception as e:
        print(f"Error: {e}")
    # DB ����
    finally:
        connection.close()





# id, n�� �Է��ϸ� �ش� id�� genres�� n�� ��ŭ ����Ʈ�� ��ȯ
def get_n_genres_by_id(movie_id, n):
    # DB ����
    connection = pymysql.connect(
        host="localhost",
        user="username",
        password="password",
        db="database_name",
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor
        )

    # �ش� ��ȭ�� genre�� n��ŭ list�� ��ȯ
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM movies WHERE movie_id=movie_id LIMIT %s"
            cursor.execute(sql, n)
            result = cursor.fetchmany(n)
            return [r['genre'] for r in result]
    # ���� ó��
    except Exception as e:
        print(f"Error: {e}")
    # DB ���� ����
    finally:
        connection.close()





# rating�� ���� ���� n���� ��ȭ���� ��ȯ
def get_top_n_movies(n):
    # DB ����
    connection = pymysql.connect(
        host="localhost",
        user="username",
        password="password",
        db="database_name",
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor
        )

    # �ش� genre�� title�� count��ŭ list�� ��ȯ
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM genre ORDER BY rating LIMIT %s"
            cursor.execute(sql, n)
            result = cursor.fetchmany(n)
            return [r['title'] for r in result]
    # ���� ó��
    except Exception as e:
        print(f"Error: {e}")
    # DB ���� ����
    finally:
        connection.close()


        


# �ش� genre�� rating�� ���� ���� n���� ��ȭ���� ��ȯ
def get_top_n_movies_by_genre(genre, n):
    # DB ����
    connection = pymysql.connect(
        host="localhost",
        user="username",
        password="password",
        db="database_name",
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor
        )

    # �ش� genre�� title�� count��ŭ list�� ��ȯ
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM genre ORDER BY rating LIMIT %s"
            cursor.execute(sql, (genre, n))
            result = cursor.fetchmany(n)
            return [r['title'] for r in result]
    # ���� ó��
    except Exception as e:
        print(f"Error: {e}")
    # DB ���� ����
    finally:
        connection.close()





# ��� �帣�� list�� ��ȯ
def get_genres():
    # DB ����
    connection = pymysql.connect(
        host="localhost",
        user="username",
        password="password",
        db="database_name",
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor
        )

    # �ش� genre�� title�� count��ŭ list�� ��ȯ
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM movie_classification WHERE id=%s"
            cursor.execute(sql, ('genres'))
            result = cursor.fetchall()
            return [r['genre'] for r in result]
    # ���� ó��
    except Exception as e:
        print(f"Error: {e}")
    # DB ���� ����
    finally:
        connection.close()





# ��õ ��ȭ��� ��ȯ
def get_movie_recommendation_list():
    list = {"a", "b", "c"}

    return list