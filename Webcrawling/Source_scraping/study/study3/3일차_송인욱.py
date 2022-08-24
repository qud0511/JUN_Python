from collections import defaultdict
from typing import Dict

import requests
from bs4 import BeautifulSoup


class Website:
    def __init__(self, url, menue="", option="", name=""):
        self.name = name  # 웹 사이트 이름: 네이버 금융
        self.url = url  # 웹 사이트 주소: https://finance.naver.com
        self.menue = menue  # 웹 사이트 매뉴: /sise/sise_market_sum.naver?&page=, https://finance.naver.com/item/main.naver?code=
        self.option = option  # 옵션: 페이지 or 코드 등등
        self.fullUrl = url + menue + str(option)  # 최종 주소

    def get_html(self):
        try:
            req = requests.get(self.fullUrl)
        except requests.exceptions.RequestException:
            return None

        return BeautifulSoup(req.text, "html.parser")


class Table:
    def __init__(self, html, url, menue, tableTag, linkTag):
        self.html = html
        self.url = url  # 테이블 찾을 url
        self.menue = menue  # 테이블 찾을 매뉴
        self.tableTag = tableTag  # 테이블 태그 table.type_2
        self.linkTag = linkTag  # 링크가 있는 태그 a.tltle
        self.dict_data = defaultdict(list)
        self.fullUrl = url + menue
        self.stocks = []
        self.links = []

    def make_data(self, num: int, absolut=True):
        table = self.html.select_one(self.tableTag)
        fullData = table.select(self.linkTag)

        if absolut:
            for data in fullData:
                self.stocks.append(data.text)
                self.links.append(data["href"])
        else:
            for data in fullData:
                self.stocks.append(data.text)
                self.links.append(self.url + data["href"])

        for stock in self.stocks[:num]:
            self.dict_data[stock]
            index = self.stocks.index(stock)
            self.dict_data[stock].append(self.links[index])
        return self.dict_data


def clawer(findTag, valuetag, dict_data):

    stocks = list(dict_data.keys())
    links = list(dict_data.values())

    for link in links:
        a = Website(link[0]).get_html()
        result = a.select_one(findTag).select(valuetag)
        for i in result:
            link.append(i.text)
    data = dict(zip(stocks, links))
    return data


def run_program(data: Dict):
    while True:
        print("-" * 30)
        print("[네이버 코스피 상위10대 기업 목록]")
        print("-" * 30)

        stocks = list(data.keys())

        for i in stocks:
            len = stocks.index(i)
            print("{0:2d} {1}".format(len + 1, i))

        num = int(input("주가를 검색할 기업의 번호를 입력하세요(-1: 종료): "))
        if num == -1:
            break

        stock = stocks[num - 1]
        result = data[stock]

        print(result[0])
        print(": ".join(result[2].split()))
        print(result[3].split()[1])
        print(result[4].split()[0] + ":", result[4].split()[1])
        print(": ".join(result[5].split()))
        print(": ".join(result[6].split()))
        print(": ".join(result[7].split()))
        print(": ".join(result[9].split()))

        input("계속하려면 아무키나 누르세요(-1: 종료): ")


naver_fin = Website("https://finance.naver.com", "/sise/sise_market_sum.naver?&page=", "1")

naver_high = Table(naver_fin.get_html(), naver_fin.url, naver_fin.menue + naver_fin.option, "table.type_2", "a.tltle")
naver_high_ten = naver_high.make_data(10, absolut=False)

result = clawer("dl.blind", "dd", naver_high_ten)
run_program(result)
