import sqlite3
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

db_path = "./share/"
db_name = "movie_data.db"
similarity_matrix_file = "similarity_matrix.npy"


def get_movie_data():
    con = sqlite3.connect(db_path + db_name)
    con.row_factory = sqlite3.Row
    cursor = con.cursor()

    query = '''SELECT movieCd, prdtYear, typeNm, prdtStatNm, nationAlt, genreAlt,
                      peopleNm, companyCd
               FROM movies
               ORDER BY movieCd ASC
    '''

    result = cursor.execute(query).fetchall()
    cursor.close()
    con.close()

    return result

def calculate_cosine_similarity(movie_data):
    # ��ȭ ����
    num_movies = len(movie_data)

    # ������ �迭 �ʱ�ȭ
    similarity_matrix = np.zeros((num_movies, num_movies))

    for i in range(num_movies):
        for j in range(num_movies):
            if i == j:
                similarity_matrix[i][j] = 0
                continue

            # i��°�� j��° ��ȭ ������ ��������
            movie1 = movie_data[i]
            movie2 = movie_data[j]

            # ��ȭ �����Ϳ��� �ʿ��� ���� ����
            features1 = [movie1["prdtYear"], movie1["typeNm"], movie1["prdtStatNm"],
                         movie1["nationAlt"], movie1["genreAlt"], movie1["peopleNm"],
                         movie1["companyCd"]]
            features2 = [movie2["prdtYear"], movie2["typeNm"], movie2["prdtStatNm"],
                         movie2["nationAlt"], movie2["genreAlt"], movie2["peopleNm"],
                         movie2["companyCd"]]

            # �ڻ��� ���絵 ���
            similarity = cosine_similarity([features1], [features2])[0][0]
            similarity_matrix[i][j] = similarity

    return similarity_matrix

# ��ȭ ������ ��������
movies = get_movie_data()

# �ڻ��� ���絵 ���
similarity_matrix = calculate_cosine_similarity(movies)

# ��� ����
np.save(similarity_matrix_file, similarity_matrix)