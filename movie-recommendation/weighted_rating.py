# weighted rating 계산해서 db 형태로 저장
# 250위 안에 들기 위한 최소 평점수 일단 500으로 설정
import sqlite3

db_path = "./share/"
db_name = "movie_data.db"

def weighted_rating(movieCd, minVoteCount, meanVoteCount, meanRating):
    con = sqlite3.connect(db_path + db_name)
    cursor = con.cursor()
    query = '''SELECT movieRating, voteCount
               FROM movies
               WHERE movieCd = ?
    '''

    cursor.execute(query, (movieCd,))
    wr = cursor.fetchone()
    cursor.close()
    con.close()

    if wr is None:
        return None

    movieRating, voteCount = wr

    result = (voteCount / (voteCount + minVoteCount)) * meanRating + (minVoteCount / (voteCount + minVoteCount)) * meanVoteCount

    return result

def calculate_mean_vote_rating():
    con = sqlite3.connect(db_path + db_name)
    cursor = con.cursor()

    # voteCount와 movieRating 값의 평균을 계산하는 쿼리
    query = '''SELECT AVG(voteCount) AS mean_vote_count, AVG(movieRating) AS mean_movie_rating
               FROM movies
    '''

    cursor.execute(query)
    result = cursor.fetchone()

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

    # 영화 데이터 가져오기
    query = '''SELECT movieCd
               FROM movies
    '''
    cursor.execute(query)
    movieCds = cursor.fetchall()

    # Weighted rating 계산 및 저장
    for movieCd in movieCds:
        weighted_rating_value = weighted_rating(movieCd[0], minVoteCount, meanVoteCount, meanRating)
        if weighted_rating_value is not None:
            update_query = '''UPDATE movies
                              SET weightedRating = ?
                              WHERE movieCd = ?
            '''
            cursor.execute(update_query, (weighted_rating_value, movieCd[0]))

    con.commit()
    cursor.close()
    con.close()

    print("Weighted ratings calculated and saved.")


if __name__ == '__main__':
    calculate_and_save_weighted_ratings()
