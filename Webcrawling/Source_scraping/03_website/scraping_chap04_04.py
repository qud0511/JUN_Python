'''
4.3.2 링크를 통한 사이트 크롤링
'''
import requests.exceptions
from bs4 import BeautifulSoup
import re

class Website:

    def __init__(self, name, url, targetPattern, absoluteUrl, titleTag, bodyTag):
        self.name = name
        self.url = url
        self.targetPattern = targetPattern
        self.absoluteUrl = absoluteUrl
        self.titleTag = titleTag
        self.bodyTag = bodyTag

class Content:

    def __init__(self, url, title, body):
        self.url = url
        self.title = title
        self.body = body

    def print(self):
        print('[URL]: {}'.format(self.url))
        print('[TITLE]: {}'.format(self.title))
        print('[BODY]:\n{}'.format(self.body))

class Crawler:
    def __init__(self, site):
        self.site = site # Website 객체
        self.visited = []

    def getPage(self, url):
        try:
            req = requests.get(url)
        except requests.exceptions.RequestException:
            return None
        return BeautifulSoup(req.text, 'html.parser')

    def safeGet(self, pageObj, selector):
        selectedElems = pageObj.select(selector)
        if selectedElems is not None and len(selectedElems) > 0:
            return '\n'.join([elem.get_text() for elem in selectedElems])
        else:
            return ''

    def safeGetBody(self, pageObj, bodyTag):
        bodyElems = pageObj.find_all('p', class_= re.compile(bodyTag))
        bodyText = ''
        if bodyElems is not None and len(bodyElems) > 0:
            for body in bodyElems:
                bodyText += body.get_text() + '\n'
            return bodyText
        else:
            return ''

    def parse(self, url):
        '''
        titleTag와 bodyTag를 검색해서 화면 출력
        '''
        bs = self.getPage(url)
        if bs is not None:
            title = self.safeGet(bs, self.site.titleTag)
            #body = self.safeGet(bs, self.site.bodyTag)
            body = self.safeGetBody(bs, self.site.bodyTag)
            if title != '' and body != '':
                content = Content(url, title, body)
                content.print()

    def crawl(self):
        '''
        사이트 홈페이지에서 페이지를 가져옴
        '''
        bs = self.getPage(self.site.url)
        targetPages = bs.find_all('div', class_ = re.compile(self.site.targetPattern))

        for targetPage in targetPages:
            targetPage = targetPage.find('a')['href']
            if targetPage not in self.visited:
                self.visited.append(targetPage)

                if not self.site.absoluteUrl:
                    targetPage = '{}{}'.format(self.site.url, targetPage)

                self.parse(targetPage)

link_pattern = '^media-story-card__placement-container+'
body_pattern = '^text__text__+'

reuters = Website('Reuters',                # Website.name
                  'https://www.reuters.com',# Website.url
                  link_pattern,             # Website.targetPattern
                  False,                    # Website.absoluteUrl
                  'h1',                     # Website.titleTag
                  body_pattern)             # Website.bodyTag

crawler = Crawler(reuters)
crawler.crawl()