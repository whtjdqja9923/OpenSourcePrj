from movie_crawler.kofic_repo import get_filmo, get_movie, get_people
from movie_crawler.kofic_repo import movie_data, people_data, companys, directors

# api_key = "1786ab654f52342e30fcd571ce235d0f"
api_key = "50df7d3ee010d7e5b91a293d2e5eba87"
kofic_api_url = {"searchMovieList":"http://kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieList.json?", \
                "searchPeopleList":"http://kobis.or.kr/kobisopenapi/webservice/rest/people/searchPeopleList.json?", \
                "searchMovieInfo":"http://kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieInfo.json?"}

db_path = "./share/"
db_name = "movie_data.db"

