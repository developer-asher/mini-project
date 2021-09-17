from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

from selenium import webdriver
from time import sleep
from bs4 import BeautifulSoup
from pymongo import MongoClient

# client = MongoClient('3.34.138.243', 27017, username="test", password="test")
client = MongoClient('localhost', 27017)
db = client.wherewego

# ChromeDriver로 접속, 자원 로딩시간 3초
driver = webdriver.Chrome('./chromedriver')

# 영화
url = "https://www.gocamping.or.kr/bsite/camp/info/list.do?listTy=TAG&searchTagCode=&searchAnimalCmgCl=CL02"

scroll_down = "window.scrollTo(0, document.body.scrollHeight);"

driver.get(url)  # 드라이버에 해당 url의 웹페이지를 띄웁니다.
sleep(1)  # 페이지가 로딩되는 동안 1초 간 기다립니다.

reqhome = driver.page_source
soupH = BeautifulSoup(reqhome, 'html.parser')

li_soup = soupH.select_one('#cont_inner > div > div.paging > ul > li:last-child > a')['href']
li_len = len(li_soup)
li_index = li_soup[li_len - 2:li_len]  # 젤 밑의 페이지갯수 숫자
print(li_index)
driver.quit()

for k in range(1, int(li_index) + 1):
    # int(li_index) + 1
    driver = webdriver.Chrome('./chromedriver')
    surl = 'https://www.gocamping.or.kr/bsite/camp/info/list.do?pageUnit=10&searchKrwd=&listOrdrTrget=last_updusr_pnttm&searchAnimalCmgCl=CL02&pageIndex=' + str(
        k)
    driver.get(surl)  # 드라이버에 해당 url의 웹페이지를 띄웁니다.
    sleep(1)  # 페이지가 로딩되는 동안 1초 간 기다립니다.
    req1 = driver.page_source
    soup1 = BeautifulSoup(req1, 'html.parser')
    licountsoup = soup1.select('#cont_inner > div > div.camp_search_list > ul > li')
    camp_count = len(licountsoup)  # 캠프링크의 숫자

    for i in range(1, camp_count + 1):
        btn_info = driver.find_element_by_css_selector(
            '#cont_inner > div > div.camp_search_list > ul > li:nth-child(' + str(i) + ') > div > div > h2 > a')
        btn_info.click()
        sleep(1)
        req = driver.page_source
        soup = BeautifulSoup(req, 'html.parser')
        camp_name = soup.select_one('.camp_name').text.strip().replace('\n', ' ')
        name = ' '.join(camp_name.split())
        viewsoup = soup1.select_one('#cont_inner > div > div.camp_search_list > ul > li:nth-child(' + str(
            i) + ') > div > div > p > span.item_t03').text
        view = viewsoup.split()[1]
        location = soup.select_one(
            '#cont_inner > div.sub_layout.layout > article > header > div > div.cont_tb > table > tbody > tr:nth-child(1) > td').text
        gourlsoup = soup1.select_one(
            '#cont_inner > div > div.camp_search_list > ul > li:nth-child(' + str(i) + ') > div > div > h2 > a')['href']
        homepageurl = 'https://www.gocamping.or.kr'
        gourl = homepageurl + gourlsoup

        img = homepageurl + \
              soup.select_one('#cont_inner > div.sub_layout.layout > article > header > div > div.img_b > img')['src']
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

        doc = {
            'name': name,
            'img': img,
            'location': location,
            'tag': tag,
            'gourl': gourl,
            'view': view
        }

        db.campinfos.insert_one(doc)
        driver.execute_script("window.history.go(-1)")
        sleep(1)
    driver.quit()