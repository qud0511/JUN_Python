from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
import re

driver = webdriver.Chrome()
driver.get('https://www.coffeebeankorea.com/store/store.asp')

# execute_script('script이름', 'args')
driver.execute_script('storeLocal2', '서울')

html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
#print(soup.prettify()) # HTML 소스를 보기 좋게 출력
# 매장 이름 검색
coffeebean_stores = soup.select('div.store_txt')

store_info = [] # 각 매장별 정보 저장
for store in coffeebean_stores:
    store_name = store.select_one('p.name > span')
    store_name = store_name.contents[0] # 점포명, 거리m가 같이 나와서 거리를 제거함
    store_addr = store.select_one('p.address > span').get_text().strip()
    store_phone = store.select_one('p.tel').get_text().strip()
    print(store_name, store_addr, store_phone)
    store_info.append([store_name, store_addr, store_phone])

print(store_info)

# DataFrame으로 변경
coffeebean_table = pd.DataFrame(store_info, columns=('매장이름', '주소', '전화번호'))
print(coffeebean_table.head())
# DataFrame을 csv파일로 저장 (utf-8로 인코딩)
coffeebean_table.to_csv('coffeebean_branches.csv', encoding='utf-8', mode='w', index=True)

driver.quit()

