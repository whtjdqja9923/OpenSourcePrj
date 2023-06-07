import sqlite3
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer

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

    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    con.close()

    return result

def calculate_cosine_similarity(movie_data):
    num_movies = len(movie_data)
    
    similarity_matrix = np.zeros((num_movies, num_movies))
    
    movie_descriptions = [f"{row['prdt year']} {row['type name']} {row['rep nation name']} {row['rep genre name']} {row['company code']} {row['director num']}"
                          for row in movie_data]
    
    vectorizer = CountVectorizer()
    feature_vectors = vectorizer.fit_transform(movie_descriptions)

    for i in range(num_movies):
        for j in range(i + 1, num_movies):
            
            movie1 = movie_data[i]
            movie2 = movie_data[j]
            
            features1 = feature_vectors[i].toarray()
            features2 = feature_vectors[j].toarray()
            
            similarity = cosine_similarity(features1, features2)[0][0]
            similarity_matrix[i][j] = similarity
            similarity_matrix[j][i] = similarity

    return similarity_matrix


if __name__ == '__main__':
    movies = get_movie_data()

    similarity_matrix = calculate_cosine_similarity(movies)

    np.save(similarity_matrix_file, similarity_matrix)
