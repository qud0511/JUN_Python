from bs4 import BeautifulSoup
import requests

#-----------------------------------------------------------------
# 클릭하는 곳
# 행 => tr
#-----------------------------------------------------------------

# driver = webdriver.Chrome('C:\workspace\chromedriver')
# driver.get('https://finance.naver.com/sise/sise_market_sum.naver')

html = requests.get('https://finance.naver.com/sise/sise_market_sum.naver')
soup = BeautifulSoup(html.text, 'html.parser')

tbody_tag = soup.find('tbody')
co_names = tbody_tag.find_all('tr', attrs = {'onmouseover':"mouseOver(this)"})
co_names = co_names[:10]

# 일단 리스트로 쭉 뽑아내보고, 딕셔너리는 나중에 생각
#-----------------------------------------------------------------

topTen = []
url_addr = []
http = 'https://finance.naver.com'

for name in co_names:
    aa = name.find('a').text
    topTen.append(aa)

    bb = name.find('a', {'class':'tltle'}).attrs['href']
    url_addr.append(http + bb)

# 종목별 상세정보
num_list = ['005930', '373220', '000660', '207940', '005935', '005380', '035420', '051910', '006400', '000270']
top_ten_stock = []

for num in num_list:
    html_1 = requests.get('https://finance.naver.com/item/main.naver?code={}'.format(num))
    bs = BeautifulSoup(html_1.text, 'html.parser')
    info = bs.find_all('dl', attrs={'class': 'blind'})

    name = info[0].find_all('dd')[1].text.split()[1]
    code = info[0].find_all('dd')[2].text.split()[1]
    today = info[0].find_all('dd')[3].text.split()[1]
    yesterday = info[0].find_all('dd')[4].text.split()[1]
    market = info[0].find_all('dd')[5].text.split()[1]
    high = info[0].find_all('dd')[6].text.split()[1]
    low = info[0].find_all('dd')[8].text.split()[1]

    top_ten_stock.append([name, code, today, yesterday, market, high, low])

# 출력하기

print('-'*30)
print('[네이버 코스피 상위 10대 기업 목록]')
print('-'*30)
for i in range(len(topTen)):
    print('[ {}] {}'.format(i+1, topTen[i]))

while True:
    choice = int(input('주가를 검색할 기업의 번호를 입력하세요(-1: 종료):'))

    if choice == -1:
        print('프로그램 종료')
        break

    elif choice >=1 and choice <=10:
        print(url_addr[choice - 1])
        print(f'''
        종목명:	{top_ten_stock[choice-1][0]}
        종목코드: {top_ten_stock[choice-1][1]}
        현재가: {top_ten_stock[choice-1][2]}
        전일가: {top_ten_stock[choice-1][3]}
        시가: {top_ten_stock[choice-1][4]}
        고가: {top_ten_stock[choice-1][5]}
        저가: {top_ten_stock[choice-1][6]}
        ''')


