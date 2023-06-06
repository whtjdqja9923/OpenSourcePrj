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

    cursor.execute(query, movieCd)
    wr = cursor.fetchone()

    if wr is None:
        return None

    movieRating, voteCount = wr

    result = (voteCount / (voteCount + minVoteCount)) * meanRating + (minVoteCount / (voteCount + minVoteCount)) * meanVoteCount

    return result

def calculate_mean_vote_rating():
    con = sqlite3.connect(db_path + db_name)
    cursor = con.cursor()
    
    query = '''SELECT AVG(voteCount) AS mean_vote_count, AVG(movieRating) AS mean_movie_rating
               FROM movies
               '''
    
    query = '''SELECT AVG("rating count") AS mean_vote_count, AVG(score) AS mean_movie_rating
               FROM rating
    '''

    cursor.execute(query)
    result = cursor.fetchone()

    if result is None:
        return None

    mean_vote_count = result[0]
    mean_movie_rating = result[1]

    cursor.close()
    con.close()

    return mean_vote_count, mean_movie_rating

def calculate_and_save_weighted_ratings():
    minVoteCount = 500
    meanVoteCount, meanRating = calculate_mean_vote_rating()

    con = sqlite3.connect(db_path + db_name)
    cursor = con.cursor()

    query = '''SELECT movieCd
               FROM movies
               '''
    cursor.execute("PRAGMA table_info(rating)")
    columns = cursor.fetchall()
    column_exists = any(column[1] == "weighted rating" for column in columns)

    if not column_exists:
        alter_query = '''ALTER TABLE rating
                         ADD COLUMN "weighted rating" FLOAT
        '''
        cursor.execute(alter_query)
        
    query = '''SELECT "movie code"
               FROM movie_basic
    '''
    cursor.execute(query)
    movieCds = cursor.fetchall()
    
    if movieCds is None:
        return None
    
    for movieCd in movieCds:
        weighted_rating_value = weighted_rating(movieCd, minVoteCount, meanVoteCount, meanRating)
        if weighted_rating_value is not None:
            update_query = '''UPDATE rating
                              SET "weighted rating" = ?
                              WHERE "movie code" = ?
            '''
            cursor.execute(update_query, (weighted_rating_value, movieCd))

    con.commit()
    cursor.close()
    con.close()


if __name__ == '__main__':
    calculate_and_save_weighted_ratings()
