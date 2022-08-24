html = '''
<div class="title">
<a onclick="javascript:ecommerceClickListGA('9791162245620', 'KOR', '구글 엔지니어는 이렇게 일한다                                                                       ', '한빛미디어', '3301', '타이터스 윈터스', '컴퓨터/IT &gt; 컴퓨터공학', '카테고리_KOR_3301');" 
href="javascript:makeDetailUrl('KOR','3301','9791162245620','0 ', 'N' )">
<strong>구글 엔지니어는 이렇게 일한다</strong></a>
</div>

<div class="pub_info">
<span class="author">타이터스 윈터스</span>
<span class="publication">한빛미디어</span>
<span class="publication">	 
2022.05.10	<!-- 초판일 -->
</span>
</div>

<div class="info">
<span>지난 50년의 세월과 이 책이 입증한 사실이 한 가지 있습니다. 바로 '소프트웨어 엔지니어링의 발전은 결코 정체되지 않는다'라는 것입니다. 빠른 기술 변화 속에서 소프트웨어 엔지니어링의 중요성이 더욱</span>
</div>
'''
from bs4 import BeautifulSoup
book = BeautifulSoup(html, 'html.parser')

book_title = book.find('div', attrs={'class': 'title'}).find('strong').text

book_info = book.find('div', attrs={'class':'pub_info'})
book_author = book_info.find('span', attrs={'class': 'author'}).text
book_publication = book_info.find('span', attrs={'class': 'publication'}).text
book_summary = book.find('div', attrs={'class': 'info'}).find('span').text

print('title:', book_title)
print('author:', book_author)
print('publication:', book_publication)
print('summary:', book_summary)