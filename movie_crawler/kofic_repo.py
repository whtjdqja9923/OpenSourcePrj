from dataclasses import dataclass, field

#데이터 예시
#{"movieCd":"20211567","movieNm":"수프와 이데올로기","movieNmEn":"Soup and Ideology",
# "prdtYear":"2021","openDt":"20221020","typeNm":"장편","prdtStatNm":"개봉","nationAlt":"한국",
# "genreAlt":"다큐멘터리","repNationNm":"한국","repGenreNm":"다큐멘터리",
# "directors":[{"peopleNm":"양영희"}],
# "companys":[{"companyCd":"20229503","companyNm":"㈜PLACE TO BE"},
# {"companyCd":"20229504","companyNm":"㈜나비온에어"}]}

@dataclass
class directors:
    people_name: str = ''

@dataclass
class companys:
    company_code: str = ''
    company_name: str = ''

@dataclass
class movie_data:
    movie_code: str = ''
    movie_name: str = ''
    movie_name_eng: str = ''
    prdt_year: str = ''
    open_date: str = ''
    type_name: str = ''
    prdt_stat_name: str = ''
    rep_nation_name: str = ''
    rep_genre_name: str = ''
    directors: list[directors] = field(default_factory=list)
    companys: list[companys] = field(default_factory=list)
