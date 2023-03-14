
# crowling
import random
import time
import requests
from bs4 import BeautifulSoup

# 파일 입출력
import sys


# url을 입력하면, html 을 받아온 후에, BeautifulSoup 으로 읽은 결과를 리턴함
def get_html(url) :
  rq = requests.get(url)
  if rq.status_code == 200:
    return BeautifulSoup(rq.content, 'html.parser')
  


# word(검색어)와, pagenum(홈페이지검색페이지번호, 1페이지당 15개씩 조회)를 입력하면
# 홈페이지검색결과 페이지 url 을 리턴함
def make_url(word, pagenum):
    if pagenum == 1 :
      pagenum_ = 2
    else :
      pagenum_ = pagenum
    
    startvalue = 15 * pagenum_ -29
    result_url = "https://search.naver.com/search.naver?display=15&f=&filetype=0&page=" + str(pagenum_) +'&query='+word+'&research_url=&sm=tab_pge&start='+str(startvalue)+'&where=web'

    return result_url
     

# 홈페이지 검색결과 페이지url을 입력할 경우, 검색된 전체 홈페이지 개수를 리턴해줌
def get_total_num(page):
  page_parse = get_html(page)

  list = len(page_parse.select('.lst_total > .bx'))

  return list


# 홈페이지 검색결과 페이지 내 몇 번재로 조회되는 지 , 아니면 page 수 retrun
def check_url_page(page,target_url):
  page_parse = get_html(page)
  page_li = page_parse.select('.lst_total > .bx a.txt')
  
  for idx,li in enumerate(page_li) :
    li_href = li['href'].split('/')[2]
    if li_href == target_url :
      return idx+1
  return 15





how_many_page = 15   # 최대 검색 페이지 수(페이지당 15개 홈페이지 표시)
# 아래에 조회 원하는 키워드 입력
search_words = ['키워드']

target_url = '내홈피.kr'  # 홈페이지 주소 protocol 제거 후 도메인만 입력

sys.stdout = open('./output_.txt','w') # 같은파일 덮어씀

for search_word in search_words:
    rank = 0
    print('\n 검색어 <{}>에 대해 검색중입니다.'.format(search_word))

    for i in range(how_many_page):
        page = make_url(search_word, i+1)
        if i == 0: 
            total = get_total_num(page)
            print('\n  결과값 : 총 {}의 홈페이지가 검색됩니다. '.format(total))
            
        print('     >'+ str(i+1)+'. {}번째 페이지를 검색중입니다({} / {}) '.format(i+1, i+1, how_many_page))
        
        counts = check_url_page(page,target_url)
        rank += counts
        
        if counts < 10: break
        time.sleep(1 + random.uniform(0.5,1.5))

    print('\n\n <============ 홈페이지 {} 검색결과순위 조회 ============>'.format(target_url))
    if rank < 10 * how_many_page: 
        print(' <{}> 검색결과 {}번째로 조회됩니다.(전체 홈페이지 {} 중 {}위)'.format(search_word, rank, total, rank ))
    else: 
        print(' <{}> 검색시 {}위 내에 찾을 수 없습니다.(전체 홈페이지 {})'.format(search_word, 10 * how_many_page, total))
        
    print('\n\n')
    
    
sys.stdout.close()

print('완료')