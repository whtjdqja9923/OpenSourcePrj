import sqlite3
import numpy as np

db_path = "./share/"
db_name = "database.db"


def weighted_rating(movieCd, minVoteCount, meanVoteCount, meanRating):
    con = sqlite3.connect(db_path + db_name)
    cursor = con.cursor()
    query = '''SELECT CAST(score AS FLOAT), CAST("rating count" AS FLOAT)
               FROM rating
               WHERE "movie code" = ?
    '''

    cursor.execute(query, (movieCd, ))
    wr = cursor.fetchone()

    if wr is None:
        cursor.close()
        con.close()
        return None

    movieRating, voteCount = wr

    result = (voteCount / (voteCount + minVoteCount)) * meanRating + (minVoteCount / (voteCount + minVoteCount)) * meanVoteCount
    
    cursor.close()
    con.close()

    return result

def add_column():
    con = sqlite3.connect(db_path + db_name)
    cursor = con.cursor()

    query = "PRAGMA table_info(rating)"
    cursor.execute(query)
    columns = cursor.fetchall()
    
    column_names = [column[1] for column in columns]
    if "weighted score" in column_names:
        cursor.close()
        con.close()
        return

    query = "ALTER TABLE rating ADD COLUMN 'weighted score' FLOAT"
    cursor.execute(query)

    con.commit()
    cursor.close()
    con.close()

def calculate_elements():
    con = sqlite3.connect(db_path + db_name)
    cursor = con.cursor()
    
    query = '''SELECT CAST("rating count" AS FLOAT) AS rating_count
               FROM rating WHERE "rating count" > 0
               '''

    cursor.execute(query)
    rating_counts = cursor.fetchall()

    if rating_counts is None or len(rating_counts) == 0:
        cursor.close()
        con.close()
        return None
    
    rating_counts = np.array(rating_counts)
    min_vote_count = np.percentile(rating_counts, 90)
    
    query = '''SELECT AVG(CAST("rating count" AS FLOAT)) AS mean_vote_count, AVG(CAST(score AS FLOAT)) AS mean_movie_rating
               FROM rating WHERE CAST("rating count" AS FLOAT) >= ?
               '''

    cursor.execute(query, (min_vote_count, ))
    result = cursor.fetchone()

    if result is None:
        cursor.close()
        con.close()
        return None
    
    mean_vote_count, mean_movie_rating = result

    cursor.close()
    con.close()

    return min_vote_count, mean_vote_count, mean_movie_rating

def calculate_and_save_weighted_ratings():
    minVoteCount, meanVoteCount, meanRating = calculate_elements()

    con = sqlite3.connect(db_path + db_name)
    cursor = con.cursor()
        
    query = '''SELECT "movie code"
               FROM movie_basic
    '''
    cursor.execute(query)
    movieCds = cursor.fetchall()
    
    if movieCds is None:
        cursor.close()
        con.close()
        return None
    
    for movieCd_tmp in movieCds:
        movieCd = movieCd_tmp[0]
        
        query = '''SELECT CAST("rating count" AS FLOAT)
               FROM rating WHERE "movie code" = ?
        '''
        cursor.execute(query, (movieCd, ))
        voteCount = cursor.fetchone()
        
        if voteCount is None or voteCount[0] < minVoteCount:
            update_query = '''UPDATE rating
                              SET "weighted score" = 0
                              WHERE "movie code" = ?
            '''
            cursor.execute(update_query, (movieCd, ))
            continue
        
        weighted_rating_value = weighted_rating(movieCd, minVoteCount, meanVoteCount, meanRating)
        if weighted_rating_value is not None:
            update_query = '''UPDATE rating
                              SET "weighted score" = ?
                              WHERE "movie code" = ?
            '''
            cursor.execute(update_query, (weighted_rating_value, movieCd))

    con.commit()
    cursor.close()
    con.close()


def update_weighted_rating():
    add_column()
    
    calculate_and_save_weighted_ratings()
