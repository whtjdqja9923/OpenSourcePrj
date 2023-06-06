import sqlite3
import numpy as np

db_path = "./share/"
db_name = "database.db"

similarity_matrix = np.load('similarity_matrix.npy')


def get_similar_movieCds(movieCd):
    con = sqlite3.connect(db_path + db_name)
    cursor = con.cursor()

    cursor.execute("SELECT `movie code` FROM movie_basic ORDER BY `movie code`")
    movieCds = [row[0] for row in cursor.fetchall()]
    movieCd_rank = movieCds.index(movieCd)

    top_indices = np.argsort(similarity_matrix[movieCd_rank])[-20:][::-1]

    top_movieCds = [movieCds[index] for index in top_indices]

    query = "SELECT `movie code`, `weighted rating` FROM movie_basic WHERE `movie code` IN ({})".format(",".join("?" * len(top_movieCds)))
    cursor.execute(query, top_movieCds)
    movie_ratings = {row[0]: row[1] for row in cursor.fetchall()}

    cursor.close()
    con.close()

    top_movieCds = sorted(movie_ratings.keys(), key=lambda x: movie_ratings[x], reverse=True)[:5]

    return top_movieCds

def get_top_n_movies_by_weighted_rating(n):
    con = sqlite3.connect(db_path + db_name)
    cursor = con.cursor()

    query = '''SELECT "movie code"
               FROM movie_basic
               ORDER BY "weighted rating" DESC
               LIMIT ?
    '''

    cursor.execute(query, (n,))
    results = cursor.fetchall()

    cursor.close()
    con.close()

    movie_codes = [result[0] for result in results]

    return movie_codes

def get_top_n_movies_by_genre(genre, n):
    con = sqlite3.connect(db_path + db_name)
    cursor = con.cursor()

    query = '''SELECT "movie code"
               FROM movie_basic
               WHERE "rep genre name" = ?
               ORDER BY "weighted rating" DESC
               LIMIT ?
    '''

    cursor.execute(query, (genre, n))
    results = cursor.fetchall()

    cursor.close()
    con.close()

    movie_codes = [result[0] for result in results]

    return movie_codes

def get_movie_details(movieCd):
    con = sqlite3.connect(db_path + db_name)
    cursor = con.cursor()
    
    query = '''SELECT r."score", mb."open date", d."people name", mb."rep genre name", 
               CASE WHEN mb."rep nation name" = '한국' THEN mb."movie name" ELSE mb."movie name eng" END AS "movie name",
               mb."rep nation name", mb."poster img link", c."company name"
               FROM movie_basic as mb
               LEFT JOIN companys AS c ON mb."movie code" = c."movie code"
               LEFT JOIN directors AS d ON mb."movie code" = d."movie code"
               WHERE "movie code" = ?
    '''
    
    cursor.execute(query, movieCd)
    result = cursor.fetchone()
    
    cursor.close()
    con.close()
    
    movieRating, OpenDt, director, repGenreNm, movieNm, repNationNm, posterLink, comNm = result

    return {
        "movieRating": movieRating,
        "OpenDt": OpenDt,
        "director": director,
        "repGenreNm": repGenreNm,
        "movieNm": movieNm,
        "repNationNm": repNationNm, 
        "posterLink": posterLink,
        "comNm": comNm
    }

def movieCd_to_movieNmEng(movieCd):
    con = sqlite3.connect(db_path + db_name)
    cursor = con.cursor()

    query = '''SELECT CASE WHEN "rep nation name" = '한국' THEN "movie name" ELSE "movie name eng" END AS "movie name" 
    FROM movie_basic WHERE "movie code" = ?
    '''
    cursor.execute(query, movieCd)
    result = cursor.fetchone()

    cursor.close()
    con.close()

    return result[0]

