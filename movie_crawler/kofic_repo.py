from dataclasses import dataclass, field
from datetime import date

#데이터 예시
#{"movieCd":"20211567","movieNm":"수프와 이데올로기","movieNmEn":"Soup and Ideology",
# "prdtYear":"2021","openDt":"20221020","typeNm":"장편","prdtStatNm":"개봉","nationAlt":"한국",
# "genreAlt":"다큐멘터리","repNationNm":"한국","repGenreNm":"다큐멘터리",
# "directors":[{"peopleNm":"양영희"}],
# "companys":[{"companyCd":"20229503","companyNm":"㈜PLACE TO BE"},
# {"companyCd":"20229504","companyNm":"㈜나비온에어"}]}

@dataclass
class movie_list:
    movieCd: str
    movieNm: str
    movieNmEn: str
    prdtYear: date
    openDt: date
    typeNm: str
    prdtStatNm: str
    repNationNm: str
    repGenreNm: str
    directors: list[directors()] = field(default_factory=list)
    companys: list[companys()] = field(default_factory=list)

@dataclass
class directors:
    peopleNm: str

@dataclass
class companys:
    companyCd: str
    companyNm: str