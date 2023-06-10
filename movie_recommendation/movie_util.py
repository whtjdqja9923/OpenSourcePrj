import sqlite3
import numpy as np

db_path = "./share/"
db_name = "database.db"

similarity_matrix = np.load('./share/similarity_matrix.npy')


def get_similar_movieCds(movieCd):
    con = sqlite3.connect(db_path + db_name)
    cursor = con.cursor()
    
    query = '''SELECT "movie code"
    FROM movie_detail
    ORDER BY "movie code"
    '''

    cursor.execute(query)
    movieCds = [row[0] for row in cursor.fetchall()]
    movieCd_rank = movieCds.index(movieCd)

    top_indices = np.argsort(similarity_matrix[movieCd_rank])[-20:][::-1]

    query = '''SELECT "movie code"
               FROM rating
               WHERE "movie code" IN ({})
               ORDER BY "weighted score" DESC
               LIMIT 3
    '''.format(",".join("?" * len(top_indices)))
    cursor.execute(query, [movieCds[index] for index in top_indices])
    top_movieCds = cursor.fetchall()
    top_movieCds = [movieCd[0] for movieCd in top_movieCds]

    posterLinks = []
    for movieCd in top_movieCds:
        query = '''SELECT "poster img link"
        FROM movie_basic
        WHERE "movie code" = ?
        '''
        cursor.execute(query, (movieCd, ))
        result = cursor.fetchone()
        if result:
            posterLinks.append(result[0])

    cursor.close()
    con.close()

    return top_movieCds, posterLinks

def get_top_n_movies_by_weighted_rating(n):
    con = sqlite3.connect(db_path + db_name)
    cursor = con.cursor()

    query = '''SELECT mb."movie code"
               FROM movie_basic AS mb
               LEFT JOIN rating AS r ON mb."movie code" = r."movie code"
               ORDER BY r."weighted score" DESC
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

    query = '''SELECT mb."movie code"
               FROM movie_basic AS mb
               LEFT JOIN rating AS r ON mb."movie code" = r."movie code"
               WHERE mb."rep genre name" = ?
               ORDER BY r."weighted score" DESC
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
    
    query = '''SELECT r."score", mb."open date", d."people name", mb."rep genre name", mb."movie name",
               mb."rep nation name", mb."poster img link", c."company name", md.synopsis
               FROM movie_basic AS mb
               LEFT JOIN companys AS c ON mb."movie code" = c."movie code"
               LEFT JOIN directors AS d ON mb."movie code" = d."movie code"
               LEFT JOIN rating AS r ON mb."movie code" = r."movie code"
               LEFT JOIN movie_detail AS md ON mb."movie code" = md."movie code"
               WHERE mb."movie code" = ?
    '''
    
    cursor.execute(query, (movieCd, ))
    result = cursor.fetchone()
    
    cursor.close()
    con.close()
    
    movieRating, openDt, director, repGenreNm, movieNm, repNationNm, posterLink, comNm, synopsis = result
        
    return {
        "movieRating": movieRating,
        "openDt": openDt,
        "director": director,
        "repGenreNm": repGenreNm,
        "movieNm": movieNm,
        "repNationNm": repNationNm, 
        "posterLink": posterLink,
        "comNm": comNm,
        "synopsis" : synopsis
    }

def movieCd_to_simple_info(movieCd):
    con = sqlite3.connect(db_path + db_name)
    cursor = con.cursor()

    query = '''SELECT mb."poster img link", mb."prdt year", mb."rep genre name", md."show time", r.score, mb."movie name"
    FROM movie_basic AS mb
    LEFT JOIN movie_detail AS md ON mb."movie code" = md."movie code"
    LEFT JOIN rating AS r ON mb."movie code" = r."movie code"
    WHERE mb."movie code" = ?
    '''
    cursor.execute(query, (movieCd, ))
    result = cursor.fetchone()

    posterLink, prdtYear, repGenreNm, showTime, movieRating, movieNm = result

    return {
        "posterLink": posterLink,
        "prdtYear": prdtYear,
        "repGenreNm": repGenreNm,
        "showTime" : showTime,
        "movieRating": movieRating,
        "movieNm": movieNm
    }

