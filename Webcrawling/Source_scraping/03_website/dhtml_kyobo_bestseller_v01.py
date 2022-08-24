import time
from bs4 import BeautifulSoup
import pandas as pd
from itertools import count
from selenium import webdriver

category_num = [3301, 3311, 3312, 3315, 3316]
category_dic = {3301: '컴퓨터공학', 3311: '데이터베이스', 3312: '웹프로그래밍',
                3315: '프로그래밍언어', 3316: '모바일프로그래밍'}

def get_kobomungo_data():
    #result = []
    wd = webdriver.Chrome()  # 본인의 webdriver 경로
    for category_idx in category_num:
        kobomungo_URL = "http://www.kyobobook.co.kr/categoryRenewal/categoryMain.laf?linkClass=%s&mallGb=KOR&orderClick=sgx" %str(category_idx)

        wd.get(kobomungo_URL)
        print("Category Index {}: {}".format(category_idx, category_dic.get(category_idx)))
        time.sleep(5)
        bestseller_list = []

        for page_idx in count():
            try:
                wd.execute_script("_go_targetPage('%s')" % str(page_idx + 1))
                print("Page index [%s]" % (str(page_idx + 1)))
            except Exception as e:
                break

            time.sleep(3)
            html = wd.page_source
            soupData = BeautifulSoup(html, 'html.parser')
            book_list = soupData.find_all('li', attrs={'class': 'id_detailli'})

            for book in book_list:
                # <em class="best_flag"><span>1</span></em>
                book_rank = book.find('em', attrs={'class': 'best_flag'}).find('span').string
                '''
                <div class="title">                    
                    <strong>구글 엔지니어는 이렇게 일한다</strong></a>
                </div>
                '''
                book_title = book.find('div', attrs={'class': 'title'}).find('strong').text
                '''
                    <div class="pub_info">
                    <span class="author">타이터스 윈터스</span>
                    <span class="publication">한빛미디어</span>
                    <span class="publication">	 
                        2022.05.10	<!-- 초판일 -->
                    </span>
                    </div>
                '''
                book_info = book.find('div', attrs={'class': 'pub_info'})
                book_author = book_info.find('span', attrs={'class': 'author'}).text
                book_publication = book_info.find('span', attrs={'class': 'publication'}).text
                book_summary = book.find('div', attrs={'class': 'info'}).find('span').text

                print(book_rank, book_title)

                bestseller_list.append([book_rank] + [book_title] + [book_author] +
                                       [book_publication] + [book_summary])
        # 파일 저장
        category_name = category_dic.get(category_idx) # category[0]: 분류번호
        book_table = pd.DataFrame(bestseller_list, columns=('순위', '제목', '저자', '출판사', '요약'))
        book_table.to_csv("./%s분야_베스트셀러_list.csv" % str(category_name),
                          encoding="utf-8", mode='w', index=False)

def main():
    print('교보문고 베스트셀러 크롤링 시작 ')
    get_kobomungo_data()
    print('----크롤링 종료 ------')

main()
