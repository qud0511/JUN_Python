'''
4.3.1 검색을 통한 사이트 크롤링
'''

class Content:
    def __init__(self, topic, url, title, body):
        self.topic = topic
        self.url = url
        self.title = title
        self.body = body

    def print(self):
        print('-' * 60)
        print('New article found for topic: {}'.format(self.topic))
        print('URL: {}'.format(self.url))
        print('TITLE: {}'.format(self.title))
        print('BODY:\n {}'.format(self.body))
        print('-' * 60)

class Website:
    def __init__(self, name, url, searchUrl, resultListing, resultUrl,
                 absoluteUrl, titleTag, bodyTag):
        self.name = name
        self.url = url
        self.searchUrl = searchUrl # URL에 검색어 추가
        self.resultListing = resultListing # 각 결과에 대한 정보 저장
        self.resultUrl = resultUrl # 결과에서 정확한 URL을 추출할 때 사용
        self.absoluteUrl = absoluteUrl # 절대 경로인지, 상대 경로인지 구분
        self.titleTag = titleTag
        self.bodyTag = bodyTag

import requests
from bs4 import BeautifulSoup

class Crawler:
    def getPage(self, url):
        try:
            req = requests.get(url)
        except requests.exceptions.RequestException:
            return None
        return BeautifulSoup(req.text, 'html.parser')

    def safeGet(self, pageObj, selector):
        childObj = pageObj.select(selector)
        if childObj is not None and len(childObj) > 0:
            return childObj[0].get_text()
        else:
            return ''

    def getAllBody(self, pageObj, selector):
        '''
        해당 tag를 가지는 모든 내용을 출력함
        '''
        childObj = pageObj.select(selector)
        bodyText = ""
        if childObj is not None:
            for i in range (len(childObj)):
                bodyText = bodyText + childObj[i].get_text() + '\n'
            return bodyText
        else:
            return ''

    def search(self, topic, site):
        # site: Website 객체
        print('searchUrl+topic:', site.searchUrl + topic)
        bs = self.getPage(site.searchUrl + topic)

        print('-' * 60)
        searchResults = bs.select(site.resultListing)

        print('searchResult len: ', len(searchResults))

        for result in searchResults:
            url = result.select(site.resultUrl)[0].attrs['href']
            print('전체 url:', site.url + url)
            if(site.absoluteUrl):
                bs = self.getPage(url)
            else:
                bs = self.getPage(site.url + url)
            if bs is None:
                print('Something was wrong with that page or URL. Skipping')
                return
            title = self.safeGet(bs, site.titleTag)
            #body = self.safeGet(bs, site.bodyTag)
            body = self.getAllBody(bs, site.bodyTag)

            if title != '' and body != '':
                content = Content(topic, url, title, body)
                content.print()



siteData = [
    ['O\'Reilly Media',                 # Website.name
     'http://oreilly.com',              # Website.url
     'https://www.oreilly.com/search/?query=', # Website.searchUrl: 검색 결과를 얻기 위한 URL
     'div#root',          # Website.resultListing: 검색 결과에 대한 정보를 담고 있는 박스
     'a',                 # Website.resultUrl: 결과에서 URL을 추출할 때 사용할 태그
     False,                              # Website.absoluteUrl
     'h1',                              # Website.titleTag
     'section.Content--Tg0io'      # Website.bodyTag
     ],
    ['Reuters',
     'http://reuters.com',
     'http://www.reuters.com/search/news?blob=',
     'div.search-result-content',
     'h3.search-result-title a',
     False,
     'h1',
     'div.StandardArticleBody_body_1gnLA']
]

crawler = Crawler()

siteData1 = [
    ['Reuters',                             # Website.name
     'http://reuters.com',                  # Website.url
     'http://www.reuters.com/search/news?blob=', # Website.searchUrl: 검색을 위한 URL
     'div.search-result-content',               # Website.resultListing: 검색 결과에 대한 정보를 담고 있는 박스
     'h3.search-result-title > a',                # Website.resultUrl: 결과에서 URL을 추출할 때 사용할 태그
     False,                                     # Website.absoluteUrl 사용 여부
     'h1',                                      # Website.titleTag <meta property="org:title> #203
     'p.Paragraph-paragraph-2Bgue']      # Website.bodyTag <meta property="org:description> #234
]

sites = []
for row in siteData1:
    sites.append(Website(row[0], row[1], row[2], row[3],
                         row[4], row[5], row[6], row[7]))

topics = ['Korea']
for topic in topics:
    print('GETTING INFO ABOUT: ' + topic)
    for targetSite in sites:
        crawler.search(topic, targetSite)
