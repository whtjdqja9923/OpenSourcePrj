import sqlite3
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

db_path = "./share/"
db_name = "database.db"
similarity_matrix_file = "similarity_matrix.npy"


def get_movie_data():
    con = sqlite3.connect(db_path + db_name)
    con.row_factory = sqlite3.Row
    cursor = con.cursor()

    query = '''SELECT mb."prdt year", mb."type name", mb."rep nation name", mb."rep genre name", c."company code", d."director num"
               FROM movie_basic AS mb
               LEFT JOIN companys AS c ON mb."movie code" = c."movie code"
               LEFT JOIN directors AS d ON mb."movie code" = d."movie code"
               ORDER BY mb."movie code" ASC
    '''

    result = cursor.execute(query).fetchall()
    cursor.close()
    con.close()

    return result

def calculate_cosine_similarity(movie_data):
    num_movies = len(movie_data)
    
    similarity_matrix = np.zeros((num_movies, num_movies))

    for i in range(num_movies):
        for j in range(num_movies):
            if i == j:
                similarity_matrix[i][j] = 0
                continue
            
            movie1 = movie_data[i]
            movie2 = movie_data[j]


            features1 = [movie1["prdtYear"], movie1["typeNm"], movie1["prdtStatNm"],
                         movie1["nationAlt"], movie1["genreAlt"], movie1["peopleNm"],
                         movie1["companyCd"]]
            features2 = [movie2["prdtYear"], movie2["typeNm"], movie2["prdtStatNm"],
                         movie2["nationAlt"], movie2["genreAlt"], movie2["peopleNm"],
                         movie2["companyCd"]]
            
            
            features1 = [movie1["prdt year"], movie1["type name"], movie1["rep nation name"],
                         movie1["rep genre name"], movie1["company code"], movie1["director num"]]
            features2 = [movie2["prdt year"], movie2["type name"], movie2["rep nation name"],
                         movie2["rep genre name"], movie2["company code"], movie2["director num"]]
            
            similarity = cosine_similarity([features1], [features2])[0][0]
            similarity_matrix[i][j] = similarity

    return similarity_matrix


if __name__ == '__main__':
    movies = get_movie_data()

    similarity_matrix = calculate_cosine_similarity(movies)

    np.save(similarity_matrix_file, similarity_matrix)