import re
import requests
import pandas as pd

from bs4 import BeautifulSoup


def top10(url):
	"""코스피 상위 10대 기업 목록 출력"""
	try:
		req = requests.get(url)
	except requests.exceptions.RequestException as e:
		print(e)
		return None
	else:
		bsObj = BeautifulSoup(req.text, 'html.parser')
		start_point = bsObj.select_one('tbody > tr')
		top = start_point.next_sibling.next_sibling  # 1위 종목부터 시작

		# <a> tag 안의 종목이름과 url 정보 저장
		stock_name = []
		stock_url = []
		for n in range(13):
			stock = top.select_one('td > a')
			try:
				stock_name.append(stock.text)
				stock_url.append(stock['href'])
			# 5위와 6위 사이의 <td.blank>와 <division_line> 처리 
			except AttributeError:
				pass
			top = top.next_sibling.next_sibling

		# DataFrame으로 저장
		kospiTop10 = pd.DataFrame({'종목명': stock_name, 'URL': stock_url}, index=range(1, 11))

		# 결과 출력
		print()
		print('-' * 35)
		print('[ 네이버 코스피 상위 10대 기업 목록 ]')
		print('-' * 35)
		for i, name in enumerate(kospiTop10['종목명']):
			print('[{0:2}] {1}'.format(i, name))
		print()

		return kospiTop10


def stockInfo(n, kospiTop10):
	"""종목 상세 정보 출력"""
	url = kospiTop10.loc[n, 'URL']
	absURL = 'https://finance.naver.com'  # 종목 상세정보 페이지
	req = requests.get(absURL+url)
	bsObj = BeautifulSoup(req.text, 'html.parser')
	bsObj = bsObj.select_one('dl.blind')  # 종목명 ~ 저가 정보가 있는 구간

	print(absURL+url)

	# DataFrame으로 저장 후 공백으로 단어 분리
	stock_detail = pd.DataFrame([bsObj.find(text=re.compile('종목명')),
								 bsObj.find(text=re.compile('종목코드')),
								 bsObj.find(text=re.compile('현재가')),
								 bsObj.find(text=re.compile('전일가')),
								 bsObj.find(text=re.compile('시가')),
								 bsObj.find(text=re.compile('고가')),
								 bsObj.find(text=re.compile('저가'))])
	stock_detail = stock_detail[0].str.split(expand=True)
	stock_detail = stock_detail.loc[:, :1]
	for k, v in zip(stock_detail[0], stock_detail[1]):
		print(k + ':', v)


def main():
	while True:
		if n == -1:
			print('프로그램 종료') 
			break
		else:
			# 상위 10대 기업 목록 출력
			url = 'https://finance.naver.com/sise/sise_market_sum.naver'
			top10(url)
			kospiTop10 = top10(url)

			# 선택 종목 상세 정보
			n = input('주가를 검색할 기업의 번호를 입력하세요(-1: 종료): ')
			stockInfo(n, kospiTop10)


if __name__ == '__main__':
	main()