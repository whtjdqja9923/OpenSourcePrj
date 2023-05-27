import sqlite3
import numpy as np

db_path = "./share/"
db_name = "movie_data.db"

similarity_matrix = np.load('similarity_matrix.npy')

def get_top_similarity_indices(similarity_row):
    length = len(similarity_row)
    
    # ���絵 ���� �ε����� ������ ��� ����Ʈ�� ����
    similarity_indices = list(enumerate(similarity_row))
    
    # ���絵�� �������� ������������ ����
    sorted_indices = sorted(similarity_indices, key=lambda x: x[1], reverse=True)
    
    top_indices = [index for index, _ in sorted_indices[:10]]
    
    return top_indices
    
# movieCd�� �������� ���� ��ȯ
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

# movieCd �������� ������ �ش��ϴ� movieCd ��ȯ
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
