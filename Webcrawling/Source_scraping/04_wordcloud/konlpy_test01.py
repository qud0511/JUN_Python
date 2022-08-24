'''
파이썬 형태소 분석기 비교 (KoNLPy: 코엔엘파이)
- https://dacon.io/competitions/open/235698/talkboard/404707?page=1&dtype=recent
    - Okt(), Kkma(), Komoran()
'''

from konlpy.tag import Kkma, Komoran, Okt

okt = Okt() # Open Korean Text (과거 트위터 형태소 분석기)
text = "마음에 꽂힌 칼한자루 보다 마음에 꽂힌 꽃한송이가 더 아파서 잠이 오지 않는다"

# pos(text): 문장의 각 품사를 태깅
# norm=True: 문장을 정규화, stem=True: 어간을 추출
okt_tags = okt.pos(text, norm=True, stem=True)
print(okt_tags)

# noun(text): 명사만 리턴
okt_nouns = okt.nouns(text)
print(okt_nouns)


