from kofic_repo import movie_data, movie_rating
from kofic_repo import get_movie, save_rating, save_movie_basic, save_movie_detail

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import re
from datetime import datetime

from time import sleep

tmdb_url = "https://www.themoviedb.org/search?language=ko&query="

def tmdb_crawl(m:movie_data, r:movie_rating) -> bool:
    ret = True
    #rating 기본값 세팅하기
    r.movie_code = m.movie_code
    r.max_score = "100"
    r.source = "TMDB"
    r.type = "movie"
    
    driver = selenium_init()
    
    try:    
        driver.get(tmdb_url + m.movie_name.replace(' ', '+'))
    except:
        ret = False
        return ret
    
    try:
        driver.find_element(By.XPATH, """//*[@id="main"]/section//h2[contains(text(),'""" + m.movie_name + """')]""").click()

        driver.find_element(By.XPATH, '''//*[@class="user_score_chart"]''').click()
        WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, '''//*[@id="rating_details_window"]''')))

        if m.show_time == "" or m.show_time is None:
            time = driver.find_element(By.XPATH, '''//*[@class="runtime"]''').text
            time = time.replace(' ', '')
            #시간 계산 ~h ~m / ~m
            if time.find('h') != -1:
                times = re.split('[hm]', time)
                m.show_time = str(int(times[0]) * 60 + int(times[1]))
            else:
                times = re.split('[m]', time)
                m.show_time = times[0]

        m.synopsis = driver.find_element(By.XPATH, '''//*[@class="overview"]/p''').text
        m.poster_img_link = driver.find_element(By.XPATH, '''//*[@class="poster"]//img''').get_attribute('src')
        
        r.score = driver.find_element(By.XPATH, '''//*[@class="user_score_chart"]''').get_attribute('data-percent')

        r_count = driver.find_element(By.XPATH, '''//*[@class="rating_details"]//h3[contains(text(),'Ratings')]''').text
        r_count = re.sub(r'[^0-9]', '', r_count)
        r.rating_count = r_count
    except:
      ret = False

    return ret

def selenium_init():
    webdriver_path = './lib/chrome/driver/chromedriver.exe'
    options = Options()

    options.binary_location = './lib/chrome/browser/App/Chrome-bin/Chrome.exe'
    options.add_argument('headless')
    # self.options.add_argument('--no-sandbox')
    options.add_argument('--no-default-browser-check')
    options.add_argument('--no-first-run')
    options.add_argument('--disable-gpu')
    options.add_argument('--log-level=3')
    options.add_argument("User-Agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36")
    
    return webdriver.Chrome(webdriver_path, options=options)

if __name__ == '__main__':
    import sqlite3

    db_path = "./share/"
    db_name = "movie_data.db"

    con = sqlite3.connect(db_path + db_name)
    cursor = con.cursor()
    
    query = ''' SELECT mb."movie code"
    FROM movie_basic mb
    LEFT OUTER JOIN movie_detail md ON ( mb."movie code" = md."movie code" )
    WHERE md.synopsis IS NULL or md.synopsis = ""
    ORDER BY mb."movie code" DESC
    '''
    rows = cursor.execute(query).fetchall()
    
    for row in rows:
        movies = get_movie(movie_name=row)
        movie = movies[0]
        rating = movie_rating()

        if tmdb_crawl(movie, rating):
            save_movie_basic(movie)
            save_movie_detail(movie)
            save_rating(rating)
        else:
            #오류 기록
            f = open('tmdb_crawl_fail_list.txt', 'a+', encoding='utf-8')
            f.write(datetime.now().strftime("%m.%d.%H:%M:%S") + '\t' + movie.movie_code + '\t' + movie.movie_name + '\n')
            f.close()
