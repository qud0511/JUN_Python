from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.error import URLError
from bs4 import BeautifulSoup


def existTag(url, tag):
	try:
		html = urlopen(url)
	except (HTTPError, URLError) as e:
		print(e)
		print('The server could not be found')
	try:
		bsObj = BeautifulSoup(html.read(), 'html.parser')
		value = bsObj.body.find_all(tag)
	except AttributeError as e:
		return None
	return value


def scraping_use_find(html):
	for data in html:
		print(f'[Period]: {data.find("p", class_="period-name").text}')
		print(f'[Short desc]: {data.find("p", class_="short-desc").text}')
		print(f'[Temperature]: {data.find("p", class_="temp").text}')
		img = data.find('img')
		print(f'[Image desc]: {img["title"]}')
		print('------------------------------------------------------------------')


def scraping_use_select(html):
	for data in html:
		print('[Period]: {0}'.format(data.select_one('p', {'class': 'period-name'}).text))
		print('[Short desc]: {0}'.format(data.select_one('p', {'class': 'short-desc'}).text))
		print('[Temperature]: {0}'.format(data.select_one('p', {'class': 'temp'}).text))
		img = data.select_one('img')
		print('[Image desc]: {0}'.format(img['title']))
		print('------------------------------------------------------------------')


def main():
	tag = 'p'
	value = existTag('https://forecast.weather.gov/MapClick.php?lat=37.7772&lon=-122.41', tag)
	if value is None:
		print('{0} could not be found'.format(tag))
	else:
		forecast = urlopen('https://forecast.weather.gov/MapClick.php?lat=37.7772&lon=-122.41')
		sevenday = BeautifulSoup(forecast, 'html.parser')
		sevenday = sevenday.find_all('div', {'class': 'tombstone-container'})
		print('National Weather Service Scraping')
		print('----------------------------------')
		print('[find 함수 이용]')
		print('--------------------------------------------------------------------')
		scraping_use_find(sevenday)
		print('[search 함수 이용]')
		print('--------------------------------------------------------------------')
		scraping_use_select(sevenday)


if __name__ == '__main__':
	print()
	main()