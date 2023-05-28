import sqlite3
import numpy as np

db_path = "./share/"
db_name = "movie_data.db"

similarity_matrix = np.load('similarity_matrix.npy')

# 영화코드(movieCd) -> 영화 상세정보(actors, movieRating, prdtYear, OpenDt, directors[], peopleNmEn, repGenreNm, movieNmEng) 함수 작성

def get_movie_ratings():
    con = sqlite3.connect(db_path + db_name)
    cursor = con.cursor()

    query = '''SELECT movieCd, weightedRating
               FROM movies
    '''
    cursor.execute(query)
    result = cursor.fetchall()

    cursor.close()
    con.close()

    movie_ratings = {}
    for movieCd, weightedRating in result:
        movie_ratings[movieCd] = weightedRating

    return movie_ratings

def get_recommend_movies(movieCd):
    similar_indices = np.argsort(similarity_matrix, axis=1)[:, ::-1][:, :20]

    movie_ratings = get_movie_ratings()

    top_indices = np.argsort([movie_ratings[movieCd] for movieCd in similar_indices[movieCd]])[::-1][:5]
    top_movieCds = [similar_indices[movieCd][index] for index in top_indices]

    return top_movieCds

def get_top_n_movies_by_weighted_rating(n):
    con = sqlite3.connect(db_path + db_name)
    cursor = con.cursor()

    query = '''SELECT movieCd
               FROM movies
               ORDER BY weightedRating DESC
               LIMIT ?
    '''

    cursor.execute(query, (n,))
    results = cursor.fetchall()

    cursor.close()
    con.close()

    movie_codes = [result[0] for result in results]

    return movie_codes

def get_top_movies_by_genre(genre, n):
    con = sqlite3.connect(db_path + db_name)
    cursor = con.cursor()

    query = '''SELECT movieCd
               FROM movies
               WHERE repGenreNm = ?
               ORDER BY weightedRating DESC
               LIMIT ?
    '''

    cursor.execute(query, (genre, n))
    results = cursor.fetchall()

    cursor.close()
    con.close()

    movie_codes = [result[0] for result in results]

    return movie_codes