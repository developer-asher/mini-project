from selenium import webdriver
from time import sleep

from bs4 import BeautifulSoup

from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.wherewego

# ChromeDriver로 접속, 자원 로딩시간 3초
driver = webdriver.Chrome('./chromedriver.exe')

# 고캠핑
url = "https://www.gocamping.or.kr/bsite/camp/info/list.do?listTy=TAG&searchTagCode=&searchAnimalCmgCl=CL02"

scroll_down = "window.scrollTo(0, document.body.scrollHeight);"

driver.get(url)  # 드라이버에 해당 url의 웹페이지를 띄웁니다.
sleep(1)  # 페이지가 로딩되는 동안 1초 간 기다립니다.

# btn_filter = driver.find_element_by_xpath('//*[@id="media_v4"]/div/div/div[2]/div[1]/div[2]/div[1]')
# i = 1
#cont_inner > div > div.camp_search_list > ul > li:nth-child(1) > div > div > h2 > a

# 조회수구하기
reqhome = driver.page_source
soupH = BeautifulSoup(reqhome, 'html.parser')

ul = soupH.select('#cont_inner > div > div.paging > ul > li')
print(len(ul))
lenul = len(ul)

li_soup = soupH.select_one('#cont_inner > div > div.paging > ul > li:nth-child('+str(lenul)+') > a')['href']
li_len = len(li_soup)
li_index = li_soup[li_len-2:li_len]
print(li_index)
driver.quit()
# for i in range(2, ):
homepageurl = 'https://www.gocamping.or.kr'

for k in range (1, int(li_index) + 1):
    # int(li_index) + 1
    driver = webdriver.Chrome('./chromedriver.exe')
    surl = 'https://www.gocamping.or.kr/bsite/camp/info/list.do?pageUnit=10&searchKrwd=&listOrdrTrget=last_updusr_pnttm&searchAnimalCmgCl=CL02&pageIndex='+str(k)
    driver.get(surl)  # 드라이버에 해당 url의 웹페이지를 띄웁니다.
    sleep(1)  # 페이지가 로딩되는 동안 1초 간 기다립니다.
    for i in range(1, 11):
        btn_info = driver.find_element_by_css_selector(
            '#cont_inner > div > div.camp_search_list > ul > li:nth-child(' + str(i) + ') > div > div > h2 > a')
        btn_info.click()
        sleep(1)
        req = driver.page_source
        soup = BeautifulSoup(req, 'html.parser')
        camp_name = soup.select_one('.camp_name').text.strip().replace('\n', ' ')
        name = ' '.join(camp_name.split())
        viewsoup = soupH.select_one('#cont_inner > div > div.camp_search_list > ul > li:nth-child(' + str(
            i) + ') > div > div > p > span.item_t03').text
        view = viewsoup.split()[1]
        location = soup.select_one(
            '#cont_inner > div.sub_layout.layout > article > header > div > div.cont_tb > table > tbody > tr:nth-child(1) > td').text
        gourlsoup = soupH.select_one(
            '#cont_inner > div > div.camp_search_list > ul > li:nth-child(' + str(i) + ') > div > div > h2 > a')['href']

        gourl = homepageurl + gourlsoup

        img = homepageurl + soup.select_one('#cont_inner > div.sub_layout.layout > article > header > div > div.img_b > img')['src']
        tag_pool = soup.select('#sub_title_wrap2 > div.layout > div.camp_tag > ul')


        for tags in tag_pool:
            tag = ''
            tag_ck = tags.text.replace('#', '').strip()
            # print(len(tag_ck))
            if '바다가 보이는' in tag_ck:
                tag = tag + '바다가 보이는 '
            if '수영장 있는' in tag_ck:
                tag = tag + '수영장 있는 '
            if '둘레길' in tag_ck:
                tag = tag + '둘레길 '

        print(tag)

        print(name, location, img)

        doc = {
            'name': name,
            'img': img,
            'location': location,
            'tag': tag,
            'gourl':gourl,
            'view':view
        }
        db.camp_info.insert_one(doc)
        driver.execute_script("window.history.go(-1)")
        sleep(1)
    driver.quit()
