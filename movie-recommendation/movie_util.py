import sqlite3
import numpy as np

db_path = "./share/"
db_name = "movie_data.db"

similarity_matrix = np.load('similarity_matrix.npy')

def get_top_similarity_indices(similarity_row):
    length = len(similarity_row)
    
    # 유사도 행의 인덱스와 값들을 묶어서 리스트로 생성
    similarity_indices = list(enumerate(similarity_row))
    
    # 유사도를 기준으로 내림차순으로 정렬
    sorted_indices = sorted(similarity_indices, key=lambda x: x[1], reverse=True)
    
    top_indices = [index for index, _ in sorted_indices[:10]]
    
    return top_indices
    
# movieCd의 오름차순 순서 반환
def movieCd_to_position(movieCd):
    con = sqlite3.connect(db_path + db_name)
    cursor = con.cursor()

    query = '''SELECT COUNT(*)
               FROM movies
               WHERE movieCd < ?
    '''

    cursor.execute(query, (movieCd,))
    position = cursor.fetchone()[0] + 1

    cursor.close()
    con.close()

    return position

# movieCd 오름차순 순서에 해당하는 movieCd 반환
def position_to_movieCd(position):
    con = sqlite3.connect(db_path + db_name)
    cursor = con.cursor()

    query = '''SELECT movieCd
               FROM movies
               ORDER BY movieCd ASC
               LIMIT 1 OFFSET ?'''

    cursor.execute(query, (position - 1,))
    movieCd = cursor.fetchone()[0]

    cursor.close()
    con.close()

    return movieCd
