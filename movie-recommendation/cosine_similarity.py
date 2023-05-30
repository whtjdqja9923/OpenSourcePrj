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
    # 영화 개수
    num_movies = len(movie_data)

    # 이차원 배열 초기화
    similarity_matrix = np.zeros((num_movies, num_movies))

    for i in range(num_movies):
        for j in range(num_movies):
            if i == j:
                similarity_matrix[i][j] = 0
                continue

            # i번째와 j번째 영화 데이터 가져오기
            movie1 = movie_data[i]
            movie2 = movie_data[j]

            # 영화 데이터에서 필요한 정보 추출
            features1 = [movie1["prdtYear"], movie1["typeNm"], movie1["prdtStatNm"],
                         movie1["nationAlt"], movie1["genreAlt"], movie1["peopleNm"],
                         movie1["companyCd"]]
            features2 = [movie2["prdtYear"], movie2["typeNm"], movie2["prdtStatNm"],
                         movie2["nationAlt"], movie2["genreAlt"], movie2["peopleNm"],
                         movie2["companyCd"]]

            # 코사인 유사도 계산
            similarity = cosine_similarity([features1], [features2])[0][0]
            similarity_matrix[i][j] = similarity

    return similarity_matrix

# 영화 데이터 가져오기
movies = get_movie_data()

# 코사인 유사도 계산
similarity_matrix = calculate_cosine_similarity(movies)

# 행렬 저장
np.save(similarity_matrix_file, similarity_matrix)