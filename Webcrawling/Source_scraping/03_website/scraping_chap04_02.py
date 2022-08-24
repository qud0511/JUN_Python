'''
4장. 웹 크롤링 모델
    4.2 다양한 웹사이트 레이아웃 다루기
'''

import requests
from bs4 import BeautifulSoup
import time
#
# Content 클래스 print()함수 추가
#
#
class Content:
    """
    글/페이지 전체에 사용할 기반 클래스
    """
    def __init__(self, url, title, body):
        self.url = url
        self.title = title
        self.body = body

    def print(self):
        print('URL: {}'.format(self.url))
        print('TITLE: {}'.format(self.title))
        print('BODY:\n{}'.format(self.body))
        print()

class Website:
    """
    웹사이트 구조에 관한 정보를 저장할 클래스
    """
    def __init__(self, name, url, titleTag, bodyTag):
        self.name = name
        self.url = url
        self.titleTag = titleTag
        self.bodyTag = bodyTag

class Crawler:
    def getPage(self, url):
        try:
            req = requests.get(url)
            time.sleep(2) # 페이지 요청 후 응답을 기다릴 시간
        except requests.exceptions.RequestException:
            return None
        return BeautifulSoup(req.text, 'html.parser')

    def safeGet(self, pageObj, selector):
        """
        BeautifulSoup 객체와 선택자를 받아 콘텐츠 문자열을 추출하는 함수
        """
        selectedElems = pageObj.select(selector)
        #print('{0} len: {1} '.format(selector, len(selectedElems)))
        if selectedElems is not None and len(selectedElems) > 0:
            return '\n'.join([elem.get_text() for elem in selectedElems])
        else:
            return ''


    def parse(self, site, url):
        """
        URL을 받아 콘텐츠를 추출함
        """
        bs = self.getPage(url)
        if bs is not None:
            title = self.safeGet(bs, site.titleTag)
            body = self.safeGet(bs, site.bodyTag)
            if title != '' and body != '':
                content = Content(url, title, body)
                print('-' * 100)
                content.print()

crawler = Crawler()

siteData = [
    ['O\'Reilly Media', 'http://oreilly.com', 'h1', 'div.content > div.metadata'], # 'div.content' 모두 출력
    ['Reuters', 'http://reuters.com', 'h1', 'p.Paragraph-paragraph-2Bgue'],
    ['Brookings', 'http://www.brookings.edu', 'h1', 'div.post-body']
]

websites = []
for row in siteData:
    websites.append(Website(row[0], row[1], row[2], row[3]))

crawler.parse(websites[0], 'http://shop.oreilly.com/product/0636920028154.do')
crawler.parse(websites[1], 'http://www.reuters.com/article/us-usa-epa-pruitt-idUSKBN19W2D0')
crawler.parse(websites[2],
    'https://www.brookings.edu/blog/techtank/2016/03/01/idea-to-retire-old-methods-of-policy-education/')

