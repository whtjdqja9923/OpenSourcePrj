from kofic_repo import movie_data, movie_rating

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

tmdb_url = "https://www.themoviedb.org/search?language=ko&query="

def tmdb_crawl(m:movie_data, r:movie_rating) -> bool:
    ret = True
    #rating 기본값 세팅하기
    r.movie_code = m.movie_code
    r.max_score = "100"
    r.source = "TMDB"
    r.type = "movie"
    
    options = Options()
    options.binary_location = './lib/chrome/browser/App/Chrome-bin/Chrome.exe'
    webdriver_path = './lib/chrome/driver/chromedriver.exe'

    driver = webdriver.Chrome(webdriver_path, options=options)
    
    driver.get(tmdb_url + m.movie_name.replace(' ', '+'))
    
    try:
      pass
    except:
      ret = False

    return ret
