from bs4 import BeautifulSoup
from datetime import datetime
import requests
import pandas as pd
import re

#크롤링 결과 임시 저장 리스트 선언
t_text=[]
l_text=[]
s_text=[]
d_text=[]
c_text=[]

#각 크롤링 결과 저장하기 위한 리스트 선언
title_text=[]
link_text=[]
source_text=[]
date_text=[]
contents_text=[]
#result={}
result=[]

#엑셀로 저장하기 위한 변수
RESULT_PATH='C:/2019_2/crawling_result/'
#현재시각으로 csv저장
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

    six_cleansing_contents = re.sub( 'dd> dl>','',fifth_cleansing_contents).strip()
    contents_text.append(six_cleansing_contents)


#크롤러
def crawler(maxpage,query,sort,s_date,e_date):
    s_from=s_date.replace(".","")
    e_to=e_date.replace(".","")
    page=1
    maxpage_t = (int(maxpage)-1)*10+1
    #11=2페이지,21=3페이지,31=4페이지

    #while문 통해서 반복 크롤링함
    while page <= maxpage_t:
        url="https://search.naver.com/search.naver?where=news&query="+query+ "&sort="+sort+"&ds="+s_date+"&de="+e_date+"&nso=so%3Ar%2Cp%3Afrom"+s_from+"to"+e_to+"%2Ca%3A&start=" + str(page)

        response =requests.get(url)
        html=response.text

        #뷰티풀소프의 인자값 지정
        soup = BeautifulSoup(html, 'html.parser')

        #<a>태그에서 제목과 링크주소 추출
        atags = soup.select('._sp_each_title')
        for atag in atags:
            title_text.append(atag.text)     #제목
            link_text.append(atag['href'])   #링크주소
            t_text.append(title_text) #추가한부분
            l_text.append(link_text)


        #신문사 추출
        source_lists = soup.select('._sp_each_source')
        for source_list in source_lists:
            source_text.append(source_list.text)    #신문사
            s_text.append(source_text)

        #날짜 추출
        date_lists = soup.select('.txt_inline')
        for date_list in date_lists:
            test=date_list.text
            date_cleansing(test)  #날짜 정제 함수사용
            d_text.append(date_text)

        #본문요약본
        contents_lists = soup.select('ul.type01 dl')
        for contents_list in contents_lists:
            #print('==='*40)
            #print(contents_list)
            contents_cleansing(contents_list) #본문요약 정제화
            c_text.append(contents_text)


        #모든 리스트 딕셔너리형태로 저장
        #result= {"date" : date_text , "title":title_text ,  "source" : source_text ,"contents": contents_text ,"link":link_text }
        #딕셔너리형태를 리스트로 지정

        #페이지출력, 주석처리가능
        print(page)

        #문자열 리스트로 만든다
        #final = [date_text,title_text,source_text,contents_text,link_text]
        #ff=final

        #df = pd.DataFrame(result)  #df로 변환
        page += 10


    # 새로 만들 파일이름 지정
    #outputFileName = '%s-%s-%s  %s시 %s분 %s초.csv' % (now.year, now.month, now.day, now.hour, now.minute, now.second)
    #df.to_csv(RESULT_PATH+outputFileName,encoding='utf-8-sig')
    #dataframe을 csv로 저장


def main():

    #크롤링할 페이지 수
    # 1페이지는 1, 2페이지는 11 , 3페이지는 21, 4페이지는 31
    maxpage ='5' #최대 100페이지 크롤링, 여기 숫자수정하면 됨

    #범죄 키워드 리스트, 키워드 수정가능
    crime = ['음주운전','탈세','성폭행','구속','마약','처벌','혐의']

    #crime 리스트를 문자열로 변환
    res=(' '.join(crime))

    #이부분 수정되어야함, 가수이름 문자열로 넘겨받음
    query=input("검색어 입력: ")

    #검색키워드+문자열
    query=query+res

 #   sort=input("뉴스 검색 방식 입력(관련도순0/최신수1/오래된순2): ")
    sort='0' #관련도순으로 크롤링

    #s_date=input("시작날짜 입력(2019.01.04): ")
    s_date='2018.01.01'

#    e_date=input("끝날짜 입력(2019.01.05): ")
    e_date='2019.12.19'
    # 크롤러 실행
    crawler(maxpage,query,sort,s_date,e_date)

   #결과값 담는 리스트
    result2 = []
    rdate=[]
    rtitle=[]
    rcontent=[]
    rlink=[]

    #for문 돌려서 리스트에 추가
    for j in range(len(date_text)):
        for i in range(len(date_text)):
            rdate.append(date_text[i])
        for i in range(len(date_text)):
            rtitle.append(title_text[i])
        for i in range(len(date_text)):
            rcontent.append(contents_text[i])
        for i in range(len(date_text)):
            rlink.append(date_text[i])
        for i in range(len(date_text)):
            result=[rdate[i],rtitle[i],rcontent[i],rlink[i]]
            result2.append(result)
    print(result2) #print



main()