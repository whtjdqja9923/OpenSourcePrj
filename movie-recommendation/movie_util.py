import sqlite3
import numpy as np

db_path = "./share/"
db_name = "movie_data.db"

similarity_matrix = np.load('similarity_matrix.npy')


def get_similar_movieCds(movieCd):
    con = sqlite3.connect(db_path + db_name)
    cursor = con.cursor()

    cursor.execute("SELECT movieCd FROM movies ORDER BY movieCd")
    movieCds = [row[0] for row in cursor.fetchall()]
    movieCd_rank = movieCds.index(movieCd)

    top_indices = np.argsort(similarity_matrix[movieCd_rank])[-20:][::-1]

    top_movieCds = [movieCds[index] for index in top_indices]

    query = "SELECT movieCd, weightedRating FROM movies WHERE movieCd IN ({})".format(",".join("?" * len(top_movieCds)))
    cursor.execute(query, top_movieCds)
    movie_ratings = {row[0]: row[1] for row in cursor.fetchall()}

    cursor.close()
    con.close()

    top_movieCds = sorted(movie_ratings.keys(), key=lambda x: movie_ratings[x], reverse=True)[:5]

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

def get_top_n_movies_by_genre(genre, n):
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

def get_movie_details(movieCd):
    con = sqlite3.connect(db_path + db_name)
    cursor = con.cursor()
    
    query = '''SELECT actors, movieRating, prdtYear, OpenDt, directors, repGenreNm, movieNmEng
               FROM movies
               WHERE movieCd = ?
    '''
    
    cursor.execute(query, (movieCd,))
    result = cursor.fetchone()
    
    cursor.close()
    con.close()
    
    actors, movieRating, prdtYear, OpenDt, directors, repGenreNm, movieNmEng = result
    
    director_names = [director["peopleNm"] for director in directors]
    actor_names = [actor["peopleNm"] for actor in actors]

    return {
        "actors": actor_names,
        "movieRating": movieRating,
        "prdtYear": prdtYear,
        "OpenDt": OpenDt,
        "directors": director_names,
        "repGenreNm": repGenreNm,
        "movieNmEng": movieNmEng
    }

def movieCd_to_movieNmEng(movieCd):
    con = sqlite3.connect(db_path + db_name)
    cursor = con.cursor()

    query = "SELECT movieNmEng FROM movies WHERE movieCd = ?"
    cursor.execute(query, (movieCd,))
    result = cursor.fetchone()

    cursor.close()
    con.close()

    return result[0]