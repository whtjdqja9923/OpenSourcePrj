import sqlite3

db_path = "./share/"
db_name = "database.db"


def weighted_rating(movieCd, minVoteCount, meanVoteCount, meanRating):
    con = sqlite3.connect(db_path + db_name)
    cursor = con.cursor()
    query = '''SELECT score, "rating count"
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

def calculate_elements():
    con = sqlite3.connect(db_path + db_name)
    cursor = con.cursor()
    
    query = '''SELECT "rating count"
               FROM rating
               '''

    cursor.execute(query)
    result = cursor.fetchone()

    if result is None:
        cursor.close()
        con.close()
        return None
    
    min_vote_count = result.quantie(0.9)
    
    query = '''SELECT AVG("rating count") AS mean_vote_count, AVG(source) AS mean_movie_rating
               FROM rating WHERE "rating count" >= ?
               '''

    cursor.execute(query, min_vote_count)
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
        weighted_rating_value = weighted_rating(movieCd, minVoteCount, meanVoteCount, meanRating)
        if weighted_rating_value is not None:
            update_query = '''UPDATE rating
                              SET score = ?
                              WHERE "movie code" = ?
            '''
            cursor.execute(update_query, (weighted_rating_value, movieCd))

    con.commit()
    cursor.close()
    con.close()


if __name__ == '__main__':
    calculate_and_save_weighted_ratings()
