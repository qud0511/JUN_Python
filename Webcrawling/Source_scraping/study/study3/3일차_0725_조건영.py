# 네이버 증시 정보 크롤링
'''
https://finance.naver.com/sise/sise_market_sum.naver에서 7월 25일의
주가의 시가총액 탑 10개의 회사이름과 URL정보를 리스트에 저장하고
https://finance.naver.com/URL정보의 사이트에 가서 종목명, 종목코드, 현재가, 전일가, 시가, 고가, 저가의
총 7개의 항목의 데이터를 찾아 크롤링하여 출력해보기
'''

# 모듈
from bs4 import BeautifulSoup
from selenium import webdriver
import time

# 기본 상수
URL = 'https://finance.naver.com'

# 시가총액 상위 10개의 이름과 URL정보 찾는 함수
def find_topten(URL):
    driver = webdriver.Chrome() # 크롬을 열고
    driver.get(URL+'/sise/sise_market_sum.naver') # 여기 사이트로
    html = driver.page_source # 해당페이지의 html을 복사
    driver.quit()
    soup = BeautifulSoup(html, 'html.parser') # html 파싱

    topten_list = soup.select('a.tltle')
    # 'div.box_type_l tbody tr td a.tltle'로 해도 됨
    # <a class="tltle" href="/item/main.naver?code=005930">삼성전자</a>, <a class="tltle" href="/item/main.naver?code=373220">LG에너지솔루션</a> ...식으로
    # 높은 순서대로 차례대로 입력되어 있다.
    # 하지만 우리가 필요한 것은 상위10개 이므로 for문을 돌려 10개만 뽑아서 필요한 이름과 URL정보만 추출하자

    add_url = [] # URL정보 담을 빈리스트
    topten_name = [] # 회사이름 담을 빈리스트
    for i in range(10): # 상위 10개를 생성할 for문
        add_url.append(topten_list[i]['href']) # href에 있는 속성값이 우리가 필요한 URL정보
        topten_name.append(topten_list[i].text) # 텍스트가 우리가 필요한 회사 이름

    return add_url, topten_name # 만든 리스트를 반환

# 각 회사별 7개 항목(현재가,종가 ...)의 데이터 추출하는 함수
def find_data(URL):
    all_data_list = [] # 한 회사의 정보가 하나의 리스트로 길이가 10인 이중리스트로 만들기 위한 빈리스트
    for ad_url in add_url: # 추가 URL이 하나씩 순서대로 입력 받음
        one_data_list = [] # 한 회사의 데이터를 입력받기 위한 빈리스트
        driver = webdriver.Chrome()
        time.sleep(2)
        driver.get(URL + ad_url) # https://finance.naver.com/item/main.naver?code=005930 사이트에 들어감
        html = driver.page_source # 해당 사이트의 html
        soup = BeautifulSoup(html, 'html.parser') # html의 파싱
        driver.quit()
        time.sleep(1)
        one_data = soup.select('dl.blind dd') # dl태그 blind클래스안의 dd태그 안에는 7개 항목이 전부 들어 있음
        for i in [1, 2, 3, 4, 5, 6, 8]: # 1부터 종목명,종목코드,현재가,전일가,시가,고가, 8에는 저가
            one_data_list.append(one_data[i].text.split()[1]) # 한회사의 데이터를 한 리스트에 담고
        all_data_list.append(one_data_list) # 전체 회사 리스트에 집어 넣기

    return all_data_list

# 메인 함수
def main(topten_name):
    print('-----------------------------------')
    print('[ 네이버 코스피 상위 10대 기업 목록 ]')
    print('-----------------------------------')
    for i in range(len(topten_name)):
        print(f"[{i+1:2}] {topten_name[i]}")

# 실행
add_url,topten_name=find_topten(URL)
all_data_list=find_data(URL)
kind=['종목명','종목코드','현재가','전일가','시가','고가','저가']

while True:
    main(topten_name)
    select=int(input('주가를 검색할 기업의 번호를 입력하세요(-1: 종료): '))
    if select==-1:
        print('프로그램 종료')
        break
    else:
        print(URL+add_url[select-1])
        for i in range(len(kind)):
            print(f"{kind[i]}: {all_data_list[select-1][i]}")










