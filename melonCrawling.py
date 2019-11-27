import requests
from bs4 import BeautifulSoup as bs
import pandas as pd

# people은 테스트 위한 것이라 없애도 됨
n = 0
people = []
music = []
name = []
pic = []
rname = []
back = []

# background contents
debut = []
birth = []
activity_tipe = []
agent = []
award = []

# request 함수
def set_request(targetSite):
    # <Response [200] 출력을 위함
    header = {'User-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko'}
    request = requests.get(targetSite, headers=header)
    # print(request)
    html = request.text
    soup = bs(html, 'html.parser')
    return soup


# <Response [406] 출력
# ㄱ: 0~1593
# 검색조건 총 몇 건인지 확인 후 10으로 나눠서 확인 => 1 부분 수정
for i in range(0, 1):
    if i == 0:
        targetSite = 'https://www.melon.com/artistplus/finder/listArtistFinderPaging.htm?startIndex=1&pageSize=10&idx=%25E3%2584%25B1&sex=&actType=&domestic=Y&tabSort=hit'
    else:
        targetSite = 'https://www.melon.com/artistplus/finder/listArtistFinderPaging.htm?startIndex={0}1&pageSize=10&idx=%25E3%2584%25B1&sex=&actType=&domestic=Y&tabSort=hit'.format(i)

    soup = set_request(targetSite)

    # 가수 이름
    artists = soup.find_all('a', {'class':'ellipsis'})
    # 가수 이미지
    images = soup.find_all('img')

    # 텍스트 부분만 추출
    for artist, image in zip(artists, images):
        n += 1
        # 가수 개인 홈페이지로 들어가기 위한 id
        move = artist['href'][artist['href'].find("('")+2:artist['href'].find("')")].rstrip()
        people.append(artist.text)
        name.append(artist.text)
        people.append(image['src'])
        pic.append(image['src'])

        # 가수 검색
        targetSite = 'https://www.melon.com/artist/song.htm?artistId={0}'.format(move)
        soup = set_request(targetSite)

        # 실명
        realnames = soup.find_all('span', {'class':'realname'})
        if len(realnames) == 0:
            people.append('')
            rname.append('')
        # 상세정보
        infos = soup.find_all('dl', {'class':'atist_info clfix'})

        # 실명
        for realname in realnames:
            people.append(realname.text.strip())
            rname.append(realname.text.strip())

        # 상세정보에서 필요없는 정보 삭제
        for info in infos:
            info = info.text.strip().replace('\n', ' ')
            info = info.replace('\t', '')
            info = info.replace('\r', '')
            info = info.replace('더보기', '')
            info = info.replace('곡재생', '')
            people.append(info.split())
            back.append(info.split())

        # 곡 수 받아오기
        num = soup.find_all('span', {'class':'text'})
        # 곡 수
        for n1 in num:
            if '발매' in n1.text:
                n2 = n1.text
        # 괄호만 추출
        number = n2[n2.find("(")+1:n2.find(")")]

        # 전체 곡 수에서 50개씩 나눠서 페이지 수 확인
        if int(number)/50%2 ==0:
           number = int(number)//50
        else:
            number = int(number) // 50 + 1

        # 곡명 받아오기
        songs = soup.find_all('a', {'class': 'fc_gray'})
        for song in songs:
            music.append(song.text)
            people.append(song.text)
        # 음악 \n으로 구분
        music.append('\n')
        # 첫번째 페이지 이후 곡을 받아옴
        if not number == 1:
            for k in range(2, number+1):
                page = (k-1)*5
                targetSite = 'https://www.melon.com/artist/songPaging.htm?startIndex={0}1&pageSize=50&listType=A&orderBy=ISSUE_DATE&artistId={1}'.format(page,move)
                soup = set_request(targetSite)
                songs = soup.find_all('a', {'class': 'fc_gray'})
                for song in songs:
                    music.append(song.text)
                    people.append(song.text)

# 정보에서 각 부분 추출
for i in range(len(back)):
    check =True
    if back[i][0] == '데뷔':
        debut.append(back[i][1])
    elif back[i][0] != '데뷔':
        debut.append('')
    if '생일' not in back[i]:
        birth.append('')
    if '활동유형' not in back[i]:
        activity_tipe.append('')
    if '소속사' not in back[i]:
        agent.append('')
    if '수상이력' not in back[i]:
        check=False
        award.append('')
    for j in range(len(back[i])):
        if back[i][j] == '소속사':
            a=j
            if check == False:
                agent.append(back[i][a+1:])
        if back[i][j] == '수상이력':
            award.append(back[i][j+1:])
            if check == True:
                agent.append(back[i][a+1:j])
        if back[i][j] == '생일':
            birth.append(back[i][j+1])
        if back[i][j] == '활동유형':
            activity_tipe.append(back[i][j+1])
            
#리스트로 합침
for num in range(len(agent)):
    if len(agent[num])>1:
        agent[num]= [' '.join(agent[num])]

for num in range(len(award)):
    if len(award[num])>1:
        award[num]= [' '.join(award[num])]
msc=[]
msc2=[]
for i in range(len(music)):
    if music[i]!='\n':
        msc.append(music[i])
    else:
        msc2.append(msc)
        msc=[]
music=msc2

# if len > 1 join 사용
print(name)
print(rname)
print(debut)
print(birth)
print(activity_tipe)
print(agent)
print(award)
print(music)
print(" ".join(agent[0]))
   # print(back[i])

"""raw_data = [{'이름': name},
            {'사진': pic},
            {'정보': back}]
data=pd.DataFrame(raw_data)"""
#data.to_csv(path_or_buf=r"C:\Users\semai\serv\m2.csv", encoding='utf_8_sig')
#print(data)
