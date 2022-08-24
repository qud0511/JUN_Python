'''
데이터크롤링과 정제
과제 #1

National Weather Service 웹사이트 (샌프란시스코 지역)
- https://forecast.weather.gov/MapClick.php?lat=37.7772&lon=-122.4168
'''

from urllib.request import urlopen
from bs4 import BeautifulSoup

def parse_use_find(html):
    '''
    find() 함수를 사용하여 html  내용을 크롤링
    :param html:
    :return:
    '''
    print('[find 함수 이용]')
    seven_day = html.find(id='seven-day-forecast')
    forecast_items = seven_day.find_all(class_='tombstone-container')
    #count = 0

    for day in forecast_items:
        if(day.find(class_='temp') is not None): # temp 항목이 있는 경우에만 수행 (if count > 0): 가능
        #if count > 0:
            period = day.find(class_='period-name').get_text()
            short_desc = day.find(class_='short-desc').get_text()
            temp = day.find(class_='temp').get_text()
            img_desc = day.find('img')['title'] # img의 'title' 속성값 가져오기

            print('-' * 80)
            print('[Period]: {0}'.format(period))
            print('[Short desc]:  {0}'.format(short_desc))
            print('[Temperature]: {0}'.format(temp))
            print('[Image desc]: {0}'.format(img_desc))
        #count += 1
    print('-' * 80)

def parse_use_select(html):
    '''
    select 함수를 사용하여 html 내용을 크롤링
    '''
    print('[select 함수 이용]')
    seven_day = html.select_one('div #seven-day-forecast')
    forecast_items = seven_day.select('.tombstone-container')

    for day in forecast_items:
        if (day.select_one('.temp') is not None):  # temp 항목이 있는 경우에만 수행
            period = day.select_one('.period-name').get_text()
            short_desc = day.select_one('.short-desc').get_text()
            temp = day.select_one('.temp').get_text()
            # img의 'title' 속성값 가져오기
            img_desc = day.select_one('img')['title']

            print('-' * 80)
            print('[Period]: {0}'.format(period))
            print('[Short desc]:  {0}'.format(short_desc))
            print('[Temperature]: {0}'.format(temp))
            print('[Image desc]: {0}'.format(img_desc))

def main():
    page = urlopen('https://forecast.weather.gov/MapClick.php?lat=37.7772&lon=-122.4168')
    html = BeautifulSoup(page.read(), 'html.parser')

    print('National Weather Service Scraping')
    print('----------------------------------')

    parse_use_find(html)
    parse_use_select(html)

main()




