from bs4 import BeautifulSoup
from datetime import datetime
import requests
import pandas as pd
import re

#각 크롤링 결과 저장하기 위한 리스트 선언
title_text=[]
link_text=[]
source_text=[]
date_text=[]
contents_text=[]
result={}

#엑셀로 저장하기 위한 변수
RESULT_PATH='C:/2019_2/crawling_result/'
now= datetime.now()


#날짜 정제화 함수
def date_cleansing(test):
    try: #지난 뉴스  #정규표현식
        pattern ='\d+.(\d+).(\d+).'

        r=re.compile(pattern)
        match=r.search(test).group(0)
        date_text.append(match)

    except AttributeError:
        #최근 뉴스
        pattern='w*(\d\w*)'
        r=re.compile(pattern)
        match=r.search(test).group(1)
        date_text.append(match)

#내용 정제화 함수
def contents_cleansing(contents):
    first_cleansing_contents = re.sub('<dl>.*?</a> </div> </dd> <dd>','',
                                      str(contents)).strip() #앞에 필요없는 부분 제거
    second_cleansing_contents = re.sub('<ul class="relation_lst">.*?</dd>','',
                                       first_cleansing_contents).strip()#뒤에 필요없는 부분 제거 (새끼기사)
    third_cleansing_contents = re.sub('<.+?','',second_cleansing_contents).strip()
    for_cleansing_contents = re.sub('trong class="hl">','',third_cleansing_contents).strip()
    fifth_cleansing_contents = re.sub('strong>','',for_cleansing_contents).strip()
    contents_text.append(fifth_cleansing_contents)


#크롤러
def crawler(maxpage,query,sort,s_date,e_date):
    s_from=s_date.replace(".","")
    e_to=e_date.replace(".","")
    page=1
    maxpage_t = (int(maxpage)-1)*10+1
    #11=2페이지,21=3페이지,31=4페이지

    while page <= maxpage_t:
        url="https://search.naver.com/search.naver?where=news&query="+query+ "&sort="+sort+"&ds="+s_date+"&de="+e_date+"&nso=so%3Ar%2Cp%3Afrom"+s_from+"to"+e_to+"%2Ca%3A&start=" + str(page)

        response =requests.get(url)
        html=response.text

        #beautifulsoup의 인자값 지정=" + e_date + "&nso=so%3Ar%2Cp%3Afrom" + s_from + "to" + e_to + "%2Ca%3A&start=" + str(page)

        response = requests.get(url)
        html = response.text

        #뷰티풀소프의 인자값 지정
        soup = BeautifulSoup(html, 'html.parser')

        #<a>태그에서 제목과 링크주소 추출
        atags = soup.select('._sp_each_title')
        for atag in atags:
            title_text.append(atag.text)     #제목
            link_text.append(atag['href'])   #링크주소

        #신문사 추출
        source_lists = soup.select('._sp_each_source')
        for source_list in source_lists:
            source_text.append(source_list.text)    #신문사

        #날짜 추출
        date_lists = soup.select('.txt_inline')
        for date_list in date_lists:
            test=date_list.text
            date_cleansing(test)  #날짜 정제 함수사용

        #본문요약본
        contents_lists = soup.select('ul.type01 dl')
        for contents_list in contents_lists:
            #print('==='*40)
            #print(contents_list)
            contents_cleansing(contents_list) #본문요약 정제화


        #모든 리스트 딕셔너리형태로 저장
        result= {"date" : date_text , "title":title_text ,  "source" : source_text ,"contents": contents_text ,"link":link_text }
        print(page)

        df = pd.DataFrame(result)  #df로 변환
        page += 10


    # 새로 만들 파일이름 지정
    outputFileName = '%s-%s-%s  %s시 %s분 %s초.csv' % (now.year, now.month, now.day, now.hour, now.minute, now.second)
    df.to_csv(RESULT_PATH+outputFileName,encoding='utf-8-sig')


def main():
    #info_main = input("="*50+"\n"+"입력 형식에 맞게 입력해주세요"+"\n"+"시작하시려면 Enter를 눌러주세요."+"\n"+"="*50)

#    maxpage = input("최대 크롤링할 페이지 수 입력하세요: ")
    maxpage = '100'

    query=input("검색어 입력: ")

 #   sort=input("뉴스 검색 방식 입력(관련도순0/최신수1/오래된순2): ")
    sort='0'

    #s_date=input("시작날짜 입력(2019.01.04): ")
    s_date='2018.01.01'

#    e_date=input("끝날짜 입력(2019.01.05): ")
    e_date='2019.11.26'
    crawler(maxpage,query,sort,s_date,e_date)

main()