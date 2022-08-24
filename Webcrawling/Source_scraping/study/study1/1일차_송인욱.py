from urllib.error import HTTPError
from urllib.request import urlopen

from bs4 import BeautifulSoup


def scraping_use_find(html):
    """find 함수 이용 스크래핑

    Args:
        html (str): 웹 사이트 url
    """
    try:
        html = urlopen(html)
    except HTTPError:
        pass

    weather = BeautifulSoup(html, "html.parser")
    a = weather.find_all("div", {"class": "tombstone-container"})

    title = "National Weather Service Scraping"
    print(title)
    print("-" * len(title))
    print("[find 함수 이용]")
    print("-" * len(title) * 2)

    for data in a:
        period = data.find("p", {"class": "period-name"}).get_text()
        short_desc = data.find("p", {"class": "short-desc"}).get_text()
        temp = data.find("p", {"class": ["temp temp-high", "temp temp-low"]}).get_text()
        image_desc = data.find("img")["alt"]

        print(f"[Period]: {period}")
        print(f"[Short desc]: {short_desc}")
        print(f"[Temperature]: {temp}")
        print(f"[Image desc]: {image_desc}")
        print("-" * len(title) * 2)


def scraping_use_select(html):
    """select 함수 이용 스크래핑

    Args:
        html (str): 웹 사이트 url
    """

    try:
        html = urlopen(html)
    except HTTPError:
        pass

    weather = BeautifulSoup(html, "html.parser")
    a = weather.select("div.tombstone-container")

    title = "National Weather Service Scraping"
    print(title)
    print("-" * len(title))
    print("[select 함수 이용]")
    print("-" * len(title) * 2)

    for data in a:
        period = data.select_one("p.period-name").get_text()
        short_desc = data.select_one("p.short-desc").get_text()
        temp = data.select("p.temp-high, p.temp-low")[0].get_text()
        image_desc = data.select_one("img")["alt"]

        print(f"[Period]: {period}")
        print(f"[Short desc]: {short_desc}")
        print(f"[Temperature]: {temp}")
        print(f"[Image desc]: {image_desc}")
        print("-" * len(title) * 2)


scraping_use_find("https://forecast.weather.gov/MapClick.php?lat=37.7772&lon=-122.4168")
scraping_use_select("https://forecast.weather.gov/MapClick.php?lat=37.7772&lon=-122.4168")
