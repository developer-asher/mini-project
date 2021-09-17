from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

from selenium import webdriver
from time import sleep
from bs4 import BeautifulSoup
from pymongo import MongoClient

#ec2 연결된 mongoDB에 연결
# client = MongoClient('3.34.138.243', 27017, username="test", password="test")

#로컬호스트 연결
client = MongoClient('localhost', 27017)
db = client.wherewego

# ChromeDriver로 접속, 자원 로딩시간 3초 꼭 Chrome 버전에 맞는 드라이버 사용해 주세요!
driver = webdriver.Chrome('./chromedriver.exe')

# 캠핑장 URL
url = "https://www.gocamping.or.kr/bsite/camp/info/list.do?listTy=TAG&searchTagCode=&searchAnimalCmgCl=CL02"

scroll_down = "window.scrollTo(0, document.body.scrollHeight);" #드라이버 스크롤 내리는 함수입니다.

driver.get(url)  # 드라이버에 해당 url의 웹페이지를 띄웁니다.
sleep(1)  # 페이지가 로딩되는 동안 1초 간 기다립니다.

reqhome = driver.page_source
soupH = BeautifulSoup(reqhome, 'html.parser')

li_soup = soupH.select_one('#cont_inner > div > div.paging > ul > li:last-child > a')['href']  #첫 검색페이지에서 페이지네이션 부분의 마지막 자식의 a href를 불러옵니다.
li_len = len(li_soup)       #가져온 url의 길이를 구합니다.
li_index = li_soup[li_len - 2:li_len]  # url의 마지막 2글자는 페이지네이션 된 페이지의 최대갯수를 나타냅니다.
                                        # URL에서 PageIndex를 가져오는 더 좋은 방법이 없을까 많이 고민했는데
                                        # 결국 좋은 방법이지 못했습니다. 이 경우 검색결과 페이지네이션된 페이지의
                                        # 갯수가 한자리일 경우 오류가 나버립니다... (더 좋은방법 생각해보기)
print(li_index)
driver.quit()

for k in range(1, int(li_index) + 1):   # 페이지 갯수 만큼 돌립니다

    driver = webdriver.Chrome('./chromedriver.exe')
    surl = 'https://www.gocamping.or.kr/bsite/camp/info/list.do?pageUnit=10&searchKrwd=&listOrdrTrget=last_updusr_pnttm&searchAnimalCmgCl=CL02&pageIndex=' + str(
        k)        #검색 결과가 URL 마지막 pageIndex의 숫자를 기준으로 페이지가 나뉜다는 것을 이용해 페이지를 바꿉니다
    driver.get(surl)    # 드라이버에 해당 url의 웹페이지를 띄웁니다.
    sleep(1)       # 페이지가 로딩되는 동안 1초 간 기다립니다.
    req1 = driver.page_source   #검색 후 들어가는 페이지에서의 페이지소스입니다.
    soup1 = BeautifulSoup(req1, 'html.parser')
    licountsoup = soup1.select('#cont_inner > div > div.camp_search_list > ul > li')    #캠프장 정보가 들어있는 li를 다 담아서 리스트를 만듭니다.
    camp_count = len(licountsoup)  # 리스트의 갯수를 세어 캠프장정보 나타내는 li의 갯수를 파악합니다.

    for i in range(1, camp_count + 1): #li의 갯수만큼 돌려줍니다
        #li의 번호에 따라 클릭할 수 있도록 지정합니다.
        btn_info = driver.find_element_by_css_selector(
            '#cont_inner > div > div.camp_search_list > ul > li:nth-child(' + str(i) + ') > div > div > h2 > a')
        btn_info.click()
        sleep(1)
        req = driver.page_source    #캠프장정보 detail 페이지에 들어간 후에 페이지소스를 가져옵니다.
        soup = BeautifulSoup(req, 'html.parser')

        # 클래스를 이용해서 캠프장 내임을 받아옵니다.
        camp_name = soup.select_one('.camp_name').text.strip().replace('\n', ' ')
        name = ' '.join(camp_name.split())

        # 조회수를 가져옵니다.
        viewsoup = soup1.select_one('#cont_inner > div > div.camp_search_list > ul > li:nth-child('
                                    + str(i) + ') > div > div > p > span.item_t03').text
        view = viewsoup.split()[1]

        #캠핑장 주소를 가져옵니다
        location = soup.select_one(
            '#cont_inner > div.sub_layout.layout > article > header > div > div.cont_tb > table > tbody > tr:nth-child(1) > td').text

        #gocamp연결되는 url을 가져옵니다.
        gourlsoup = soup1.select_one(
            '#cont_inner > div > div.camp_search_list > ul > li:nth-child(' + str(i) + ') > div > div > h2 > a')['href']
        homepageurl = 'https://www.gocamping.or.kr'
        gourl = homepageurl + gourlsoup     #가져온 url이 상대주소 여서 절대주소로 바꿔줍니다.

        #캠프장 이미지src를 가져옵니다. 마찬가지로 상대주소를 절대주소로 바꿉니다.
        img = homepageurl + soup.select_one('#cont_inner > div.sub_layout.layout > article > header > div > div.img_b > img')['src']

        #태그들을 리스트로 전부 가져옵니다.
        tag_pool = soup.select('#sub_title_wrap2 > div.layout > div.camp_tag > ul')

        #태그들 중 필요한 태그만 선별해서 담습니다.
        for tags in tag_pool:
            tag = ''
            tag_ck = tags.text.replace('#', '').strip()

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