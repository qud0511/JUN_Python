import os
import pandas as pd

from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.error import HTTPError, URLError


def main():
	# set branch's info as a DataFrame
	values = [[], [], [], []]
	for n in range(1, 54):
		try:
			url = f'https://www.hollys.co.kr/store/korea/korStore2.do?pageNo={n}&sido=&gugun=&store='
			html = urlopen(url)
		except (HTTPError, URLError) as e:
			print(e)
			return None
		bsobj = BeautifulSoup(html, 'html.parser')
		for tr in bsobj.find_all('tr'):
			td = tr.find_all('td')
			if td:
				values[0].append(td[0].text)
				values[1].append(td[1].text)
				values[2].append(td[3].text)
				values[3].append(td[5].text)
				hollys_branches = pd.DataFrame({'매장이름': values[1], '위치(시,구)': values[0], 
												'주소': values[2], '전화번호': values[3]})

	# display all Hollys branch
	print()
	for n in range(len()):
		print(f'[{n+1:3d}]: '
			f'매장이름: {hollys_branches["매장이름"][n]}, '
			f'지역: {hollys_branches["위치(시,구)"][n]}, '
			f'주소: {hollys_branches["주소"][n]}, '
			f'전화번호: {hollys_branches["전화번호"][n]}')
	print(f'전체 매장 수: {hollys_branches.shape[0]}')


	# save branch info as a csv file
	if not os.path.exists('./hollys_branches.csv'):	
		hollys_branches.to_csv('hollys_branches.csv', encoding='utf-8')


# Find Hollys branch by the city
def findHollys(city):
	branch = pd.read_csv('./hollys_branches.csv')
	# '서울 동작' to ['서울', '동작']
	keyword = city.split()
	# 'true' list for boolean values about each keyword
	true = []
	for k in keyword:
		true.append(branch['주소'].str.contains(k))
	true = pd.DataFrame(true).T
	
	# return [True, True] row on address column
	result = []
	for i in range(len(true)):
		if all(true.loc[i]):
			result.append(branch.loc[i, ['주소', '전화번호']])
			result = pd.DataFrame(result)
			print('-' * 20)
			print(f'검색된 매장 수: {len(result)}')
			print('-' * 20)
			for n in range(len(result)):
				print(f'[{n+1:3d}]: [\'{result["주소"][n]}\', \'{result["전화번호"][n]}\']')
	print()


if __name__ == '__main__':
	main()
	city = input('검색할 매장의 도시를 입력하세요: ')
	findHollys(city)
