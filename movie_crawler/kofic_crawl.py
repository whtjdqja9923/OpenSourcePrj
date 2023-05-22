from time import sleep

import requests
from bs4 import BeautifulSoup
import json
from kofic_repo import movie_data, directors, companys
import datetime
from datetime import datetime

api_key = "1786ab654f52342e30fcd571ce235d0f"
kofic_api_url = {"searchMovieList":"http://kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieList.json?", \
                 "searchPeopleList":"http://kobis.or.kr/kobisopenapi/webservice/rest/people/searchPeopleList.json?"}

class kofic_crawler:
    itemPerPage = "100"; #1~100사이의 수, n개 단위 호출

    def searchMovieList_crawl(self, START_PAGE, END_PAGE):
        for i in range (START_PAGE, END_PAGE+1):
            curPage = str(i)
            webpage = ''
            ext = 0
            data = movie_data()

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


            sleep(0.5) # 과부하 방지

    # def searchPeopleList_crawl(self, START_PAGE, END_PAGE):
    #     for i in range (START_PAGE, END_PAGE+1):
    #         curPage = i
    #         curPage = str(curPage)

    #         #일단 파일로 기록하고 추후에 DB에 등록하도록 변경
    #         sys.stdout = open("./moviecrawler/result/kofic_searchPeopleList_" \
    #                           + self.itemPerPage + "_" + curPage + ".json", "w", encoding="utf-8")

    #         webpage = ''
    #         ext = 0
    #         while(webpage == ''):
    #             try:
    #                 ext = ext + 1
    #                 if ext == 30: #최대 시도 횟수
    #                     break
    #                 webpage = requests.get(kofic_api_url['searchPeopleList'] + "key=" + api_key + \
    #                                        "&" + "itemPerPage=" + self.itemPerPage + \
    #                                         "&" + "curPage=" + curPage)
    #             except:
    #                 sleep(5)

    #         soup = BeautifulSoup(webpage.content, "html.parser")
    #         print(soup)

    #         sys.stdout.close()
    #         sleep(0.5) # 과부하 방지

a = kofic_crawler()
a.searchMovieList_crawl(1, 2)