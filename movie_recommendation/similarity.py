import sqlite3
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

db_path = "./share/"
db_name = "database.db"
similarity_matrix_file = "./share/similarity_matrix.npy"


def get_movie_synopses():
    con = sqlite3.connect(db_path + db_name)
    cursor = con.cursor()

    query = '''SELECT "movie code", synopsis
               FROM movie_detail
               ORDER BY "movie code" ASC
    '''

    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    con.close()

    return result


def calculate_similarity_matrix(movie_synopses):
    num_movies = len(movie_synopses)

    synopses = [synopsis for _, synopsis in movie_synopses]

    vectorizer = TfidfVectorizer()

    synopses = [synopsis if synopsis is not None else '' for synopsis in synopses]

    tfidf_matrix = vectorizer.fit_transform(synopses)

    similarity_matrix = cosine_similarity(tfidf_matrix, tfidf_matrix)
    
    similarity_matrix = np.where(np.eye(num_movies), 0, similarity_matrix)

    return similarity_matrix


def update_similarity_matrix():
    movie_synopses = get_movie_synopses()

    similarity_matrix = calculate_similarity_matrix(movie_synopses)

    np.save(similarity_matrix_file, similarity_matrix)
