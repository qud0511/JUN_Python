'''
웹 크롤링: 커피 매장 찾기
- https://www.hollys.co.kr

- 매장 찾기 페이지 url
 https://www.hollys.co.kr/store/korea/korStore2.do?pageNo=1&sido=&gugun=&store=
  - pageNo=1 ~ pageNo=53까지 모두 검색

'''

from bs4 import BeautifulSoup
from urllib.request import urlopen
import pandas as pd

branches = [] # 커피 매장 저장 리스트
end_page = 53 # 커피 매장 마지막 페이지: 53
index = 1

for page in range(1, end_page+1):
    hollys_url = 'https://www.hollys.co.kr/store/korea/korStore2.do?pageNo={0}&sido=&gugun=&store='.format(page)

    #print(hollys_url)
    html = urlopen(hollys_url)
    soup = BeautifulSoup(html, 'html.parser')
    tag_tbody = soup.find('tbody')

    for store in tag_tbody.find_all('tr'):
        store_td = store.find_all('td')

        store_city = store_td[0].string     # 매장이 있는 지역(시, 구)
        store_name = store_td[1].string     # 매장 이름
        store_address = store_td[3].text    # 매장 주소
        store_phone = store_td[5].string    # 매장 전화번호

        print('[{0:3d}]: 매장이름: {1}, 지역: {2}, 주소: {3}, 전화번호: {4}'.
              format(index, store_name, store_city, store_address, store_phone))

        branches.append([store_name] + [store_city] + [store_address] + [store_phone])
        index += 1

total_branch_number = len(branches)
print('전체 매장 수: {}'.format(total_branch_number))

#
# 크롤링한 데이터를 CSV 파일로 저장하기
# 리스트를 pandas dataframe으로 변경 -> csv 파일로 저장
#
hollys_table = pd.DataFrame(branches, columns=('매장이름', '위치(시,구)', '주소', '전화번호'))
print(hollys_table.head())
# utf-8로 인코딩
hollys_table.to_csv('hollys_branches.csv', encoding='utf-8', mode='w', index=True)

#
#    위치(시,구) 컬럼 에서 입력된 location 값 검색
#
search_city = input('찾을 매장의 도시를 입력하세요: ')
# 부산 사하구, 경기 광명시, 경기 시흥시

df['위치(시,구)'] == search_city
