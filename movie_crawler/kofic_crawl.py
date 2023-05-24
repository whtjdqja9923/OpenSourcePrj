from time import sleep
import json

import requests
from bs4 import BeautifulSoup

from kofic_repo import movie_data, directors, companys, people_data, \
    save_movie_list, save_people_list, save_movie_detail

# api_key = "1786ab654f52342e30fcd571ce235d0f"
api_key = "50df7d3ee010d7e5b91a293d2e5eba87"
kofic_api_url = {"searchMovieList":"http://kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieList.json?", \
                "searchPeopleList":"http://kobis.or.kr/kobisopenapi/webservice/rest/people/searchPeopleList.json?", \
                "searchMovieInfo":"http://kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieInfo.json?"}

class kofic_crawler:
    itemPerPage = "100"; #1~100사이의 수, n개 단위 호출

    def searchMovieList_crawl(self, START_PAGE, END_PAGE):
        for i in range (START_PAGE, END_PAGE+1):
            curPage = str(i)
            webpage = ''
            ext = 0
            data_list = [];

            while(webpage == ''):
                try:
                    ext = ext + 1
                    if ext == 30: #최대 시도 횟수
                        break
                    webpage = requests.get(kofic_api_url['searchMovieList'] + "key=" + api_key + \
                                        "&" + "itemPerPage=" + self.itemPerPage + \
                                        "&" + "curPage=" + curPage)
                except:
                    sleep(5)
            
            soup = BeautifulSoup(webpage.content, "html.parser")
            crawl_result = json.loads(soup.string)
            movie_list = crawl_result.get('movieListResult').get('movieList')

            for movie in movie_list:
                data = movie_data()

                data.movie_code = movie.get('movieCd')
                data.movie_name = movie.get('movieNm')
                data.movie_name_eng = movie.get('movieNmEn')
                data.prdt_year = movie.get('prdtYear')
                data.open_date = movie.get('openDt')
                
                data.type_name = movie.get('typeNm')
                data.prdt_stat_name = movie.get('prdtStatNm')
                data.rep_nation_name = movie.get('repNationNm')
                data.rep_genre_name = movie.get('repGenreNm')

                for d in movie.get('directors'):
                    director = directors()
                    director.people_name = d.get('peopleNm')
                    data.directors.append(director)
                
                for c in movie.get('companys'):
                    company = companys()
                    company.company_code = c.get('companyCd')
                    company.company_name = c.get('companyNm')
                    data.companys.append(company)

                data_list.append(data)

            save_movie_list(data_list)
            # sleep(0.5) # 과부하 방지

    def searchMovieInfo_crawl(self, movie_code_list:list[str]):
        for movie_code in movie_code_list:
            webpage = ''
            ext = 0

            while(webpage == ''):
                try:
                    ext = ext + 1
                    if ext == 30: #최대 시도 횟수
                        break
                    webpage = requests.get(kofic_api_url['searchMovieInfo'] + "key=" + api_key + \
                                           "&" + "movieCd=" + movie_code)
                except:
                    sleep(5)

            soup = BeautifulSoup(webpage.content, "html.parser")
            try:
                crawl_result = json.loads(soup.string)
            except:
                f = open("./searchMovieInfoerr.txt", 'a')
                f.write(movie_code + '\n')
                f.close()

                continue

            movie_info = crawl_result.get('movieInfoResult').get('movieInfo')

            data = movie_data()
            data.movie_code = movie_code
            data.movie_name_org = movie_info.get('movieNmOg')
            data.show_time = movie_info.get('showTm')

            print("working : " + movie_code, "name : " + movie_info.get('movieNm'))
            save_movie_detail(data)

            sleep(1)


    def searchPeopleList_crawl(self, START_PAGE, END_PAGE):
        for i in range (START_PAGE, END_PAGE+1):
            curPage = str(i)
            data_list = []

            webpage = ''
            ext = 0
            # while(webpage == ''):
            #     try:
            #         ext = ext + 1
            #         if ext == 30: #최대 시도 횟수
            #             break
            #         webpage = requests.get(kofic_api_url['searchPeopleList'] + "key=" + api_key + \
            #                                 "&" + "itemPerPage=" + self.itemPerPage + \
            #                                 "&" + "curPage=" + curPage)
            #     except:
            #         sleep(5)

            # soup = BeautifulSoup(webpage.content, "html.parser")
            # crawl_result = json.loads(soup.string)

            file_path = 'E:/study/MovieRecomServPrj/moviecrawler/result/' + 'kofic_searchPeopleList_100_' + curPage + '.json'
            with open(file_path, 'r', encoding='utf-8') as f:
                crawl_result = json.load(f)
            print("working : ", curPage)

            people_list = crawl_result.get('peopleListResult').get('peopleList')

            for people in people_list:
                data = people_data()

                data.people_code = people.get('peopleCd')
                data.poeple_name = people.get('peopleNm')
                data.people_name_eng = people.get('peopleNmEn')
                data.rep_role_name = people.get('repRoleNm')
                data.filmo_comapct = people.get('filmoNames')
                if people.get('filmoNames'):
                    data.filmo_names = people.get('filmoNames').split('|')
                
                data_list.append(data)

            save_people_list(data_list)
            # sleep(0.5) # 과부하 방지

if __name__ == "__main__":
    from kofic_repo import create_table_movie
    import sqlite3

    db_path = "./share/"
    db_name = "movie_data.db"

    con = sqlite3.connect(db_path + db_name)
    cursor = con.cursor()
    a = kofic_crawler()

    query = '''select mb."movie code" 
        from movie_basic mb left outer join movie_detail md 
        ON ( mb."movie code" = md."movie code" ) 
        where md."movie code" IS NULL 
        order by mb."prdt year" DESC 
        limit 1000; '''
    list = []
    for i in cursor.execute(query).fetchall():
        list.append(i[0])
    
    cursor.close()
    con.close()

    a.searchMovieInfo_crawl(list)