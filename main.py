from webbrowser import get
import discord
from discord.ext import commands
import asyncio
import json
import os
from dotenv import load_dotenv
import requests
import time
import datetime
import pytz
import random
import youtube_dl
import ffmpeg
from youtube_search import YoutubeSearch
from youtubesearchpython import *
from urllib.parse import unquote, quote_plus, urlencode
import lxml
from bs4 import BeautifulSoup
#from system import TOKEN

intents = discord.Intents.all()
bot=commands.Bot(command_prefix='/',help_command=None,intents=intents)
playlist = []
loop = False

NMJ = False # 내맘점 운영기간

@bot.event # 시작
async def on_ready():
    print(f"{bot.user.name} : on ready")
    await bot.change_presence(status=discord.Status.online, activity=discord.Game(name='/도움말'))


############################################## 【 기본 】 ##############################################

# 도움말
@bot.command()  
async def 도움말(ctx):
    embed = discord.Embed(title="SDHS 사용설명서", color=0x62c1cc) # Embed의 기본 틀(색상, 메인 제목, 설명)을 잡아줍니다
    embed.add_field(name="기본", value="`도움말`, `시간`, `따라하기`, `주사위`", inline=False)
    embed.add_field(name="음악", value="`재생`, `일시정지`, `반복`, `플레이리스트`, `삭제`, `넘기기`, `종료`", inline=False)
    embed.add_field(name="학교", value="`급식`, `시간표`, `학사일정`", inline=False)
    embed.add_field(name="특수", value="`이벤트`, `내맘점(내 맘대로 점심)`", inline=False)
    embed.add_field(name="시스템", value="`정보`", inline=False)
    await ctx.send(embed=embed)

# 시간
KRtime = datetime.datetime.now(pytz.timezone('Asia/Seoul')).strftime('%Y-%m-%d-%p-%I-%M-%S') #UTC+9
@bot.command() 
async def 시간(ctx,*,text = None): 
  if(text == None):
    await ctx.send(f"현재 시간은 [{KRtime[:4]}-{KRtime[5:7]}-{KRtime[8:10]}] {KRtime[11:13]} {KRtime[14:16]}시 {KRtime[17:19]}분 {KRtime[20:22]}초 입니다.")

# 인사
@bot.command() 
async def 안녕(ctx):
    await ctx.send('안녕하세요, 저는 강원사대부고 전용 디스코드 봇, SDHS에요. 만나서 반가워요.')

# 따라하기
@bot.command()
async def 따라하기(ctx,*,text):
    await ctx.send(text)

# 이벤트
@bot.command()
async def 이벤트(ctx,*,text):
    await ctx.send("현재 진행중인 이벤트가 없습니다.")

# 특수 中 내맘점 (내 맘대로 점심)
@bot.command(aliases=['내맘대로점심','ㄴㅁㅈ'])
async def 내맘점(ctx):
    if NMJ == True:
        await ctx.send(f"현재 {KRtime[5:7]}월 강원사대부고 내 마음대로 점심이 운영중이에요.")
        await ctx.send("n월n일까지 신청할 수 있습니다.")
        embed = discord.Embed(title="내맘점 신청",description='[링크](https://m.site.naver.com/qrcode/view.naver?v=12pq8) 에서 신청할 수 있습니다.', color=0x62c1cc)
        embed.set_image(url="https://media.discordapp.net/attachments/1034286732713132032/1036859140556988456/IMG_6958.jpg?width=473&height=631")
        await ctx.send(embed=embed)
    else:
        await ctx.send("현재 강원사대부고 내 맘대로 점심을 운영하고 있지 않아요. 다음에 다시 신청해주세요 :)")


Diceimage = ["0",
"https://media.discordapp.net/attachments/898797966666637354/998218730452549692/Dice_1.jpg",
"https://media.discordapp.net/attachments/898797966666637354/998218744054697994/Dice_2.jpg",
"https://media.discordapp.net/attachments/898797966666637354/998218749108830298/Dice_3.jpg",
"https://media.discordapp.net/attachments/898797966666637354/998218945196728360/Dice_4.jpg",
"https://media.discordapp.net/attachments/898797966666637354/998218950364111010/Dice_5.jpg",
"https://media.discordapp.net/attachments/898797966666637354/998218963538419752/Dice_6.jpg"]

# 주사위 게임
@bot.command()
async def 주사위(ctx,*,text=None):
    if text == None:
        await ctx.send("주사위를 굴리면 1~6 중 임의의 숫자가 나옵니다. /주사위 굴리기 로 이용해보세요.")
    elif text == "굴리기":
        Dice = random.randint(1,6)
        await ctx.send("주사위를 굴리는중...")
        await asyncio.sleep(2)
        embed = discord.Embed(title=f"주사위 결과는 : **{Dice}**")
        embed.set_image(url=Diceimage[Dice])
        await ctx.send(embed=embed)
    else:
        await ctx.send("잘못 입력하셨습니다.")

@bot.command(aliases=['covid19','covid-19','Covid19','Covid-19','COVID19','COVID-19'])  # !코로나 입력 시에도 실행 가능
async def 코로나(ctx):
    url = "http://ncov.mohw.go.kr/"
    response = requests.get(url)  # get 방식으로 웹 정보 받아오기
    response_code = int(response.status_code)  # 응답 코드 받기

    if response_code == 200:  # 정상 작동(코드 200 반환) 시
        soup = BeautifulSoup(response.content, 'lxml')
    else: # 오류 발생
        await ctx.send("웹 페이지 오류입니다.")

    # soup.find ()로 <div class="liveToggleOuter"> 에서 확진자 수 데이터가 들어 있는 <span class="data"> 리스트 가져오기
    today = soup.find("div", {"class": "liveToggleOuter"}).findAll("span", "before")
    today_domestic = int(today[0].text)  # 리스트 첫 번째 요소 (확진)
    accumulate_confirmed = soup.find("div", {"class": "liveNum"}).find("span", {"class": "num"}).text[4:]  # 앞에 (누적) 글자 자르기

    embed = discord.Embed(title="국내 코로나 확진자 수 현황", description="보건복지부 코로나바이러스감염증-19의 정보를 바탕으로 제작되었습니다.", color=0x005666)
    embed.add_field(name="일일 확진자",
                value=f"총 : {today_domestic}",inline=False)
    embed.add_field(name="누적 확진자", value=f"{accumulate_confirmed}명", inline=False)
    await ctx.send(embed=embed)


############################################## 【 노래 】 ##############################################


# 플레이리스트
@bot.command(aliases = ['플리'])
async def 플레이리스트(ctx):
    if len(playlist) >= 1:
        embed = discord.Embed(title="🎼 현재 재생중인 플레이리스트", color=0x62c1cc)
        if loop == True:
            embed.add_field(name='[현재 진행중인 곡]',value=f'🔁 【{playlist[0][0]}】', inline=False)
        elif loop == False:
            embed.add_field(name='[현재 진행중인 곡]',value=f'【{playlist[0][0]}】', inline=False)
        if len(playlist) > 1:
            for i in range(1,len(playlist)):
                embed.add_field(name=f'예약 {i}번째 곡', value=f'【{playlist[i][0]}】', inline=False)
        embed.set_thumbnail(url=playlist[0][2])
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title="🎼 현재 재생중인 플레이리스트", description='현재 재생중인 곡이 없습니다.', color=0x62c1cc)
        await ctx.send(embed=embed)

# 일시정지
@bot.command(aliases = ['pause','resume'])
async def 일시정지(ctx):
  if not bot.voice_clients[0].is_paused():
    bot.voice_clients[0].pause()
    await ctx.send("⏸️일시정지 되었습니다. /일시정지 를 다시 입력하면 재생됩니다.")
  elif bot.voice_clients[0].is_paused():
    bot.voice_clients[0].resume()
    await ctx.send("다시 재생합니다.")

# 반복
@bot.command()
async def 반복(ctx):
    global loop
    if loop == True:
        loop = False
        await ctx.send("반복모드를 해제합니다.")
    elif loop == False:
        loop = True
        await ctx.send("현재 곡을 🔁반복 설정합니다. /반복 을 다시 입력하면 해제됩니다.")

# 삭제
@bot.command()
async def 삭제(ctx,*,number):
    global playlist
    number = int(number)
    if len(playlist)-1 >= number:
        del playlist[number]
        await ctx.send(f"✂️{number}번째 예약곡을 삭제했습니다.")
    else:
        await ctx.send(f"{number}번째 예약곡을 찾을수 없습니다.")

# 넘기기
@bot.command(aliases = ['skip','s','스킵'])
async def 넘기기(ctx):
    global loop
    if len(playlist) == 0:
        await ctx.send("재생중인 곡이 없습니다.")
    else:
        if loop == True:
            loop = False
            await ctx.send("넘기기를 사용하여 반복모드가 해제됩니다.")
        bot.voice_clients[0].stop()
        await ctx.send("현재 재생중인 곡을 스킵합니다.")
        if len(playlist) == 0:
            await bot.voice_clients[0].disconnect()
            await ctx.send("SDHS : 노래 서비스가 종료되었습니다.")

# 종료
@bot.command()
async def 종료(ctx):
    global playlist
    global loop
    playlist = []
    loop = False
    await bot.voice_clients[0].disconnect()
    await ctx.send("SDHS : 노래 서비스가 종료되었습니다.")
    
# 노래 신청
@bot.command(aliases = ['play','p','ㅔ','wotod','WOTOD'])
async def 재생(ctx,*,keyword):
    global voice
    global playlist
    result = YoutubeSearch(keyword, max_results=1).to_dict()
    channel = ctx.author.voice.channel
    if bot.voice_clients == []:
        await channel.connect()
    voice = bot.voice_clients[0]
    titles = result[0]['title']
    url = result[0]['url_suffix']
    songjpg = result[0]['thumbnails'][0]
    print(f'<입력> : https://www.youtube.com{url}')
    playlist.append([titles,url,songjpg])
    await song_quest(titles,url,songjpg)
    await ctx.send(embed=embeds)
    if len(playlist) == 1:
        await main_of_music()
    else:
        pass

# 노래 사진&정보 출력
async def song_quest(titles,url,songjpg):
    global embeds
    embeds = discord.Embed(title="SDHS PLAYLIST", description=f"노래가 신청되었습니다.\n[클릭](https://www.youtube.com{url})하여 노래 영상 링크로 이동할 수 있습니다.", color=0x62c1cc)
    embeds.add_field(name='제목',value=f'【{titles}】',inline=False)
    embeds.set_image(url=songjpg)

# 메인 보드 (시스템 중간처리)
async def main_of_music():
    while True:
        if len(playlist) >= 1:
            await asyncio.sleep(0.1)
            while voice.is_playing() or voice.is_paused():
                await asyncio.sleep(0.1)
            await song_start(voice, playlist[0][1])
        else:
            break

# 노래 실제 재생 - 재생 시작시 플레이리스트에서 삭제
async def song_start(voice, url):
    global playlist
    if not voice.is_playing() and not voice.is_paused():
        ydl_opts = {'format': 'bestaudio'}
        FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f'https://www.youtube.com{url}', download=False)
            URL = info['formats'][0]['url']
        voice = bot.voice_clients[0]
        voice.play(discord.FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
        while voice.is_playing() or voice.is_paused():
            await asyncio.sleep(0.1)
        if loop == True:
            pass
        elif loop == False:
            del playlist[0]
    else:
        while voice.is_playing() or voice.is_paused():
            await asyncio.sleep(0.1)


############################################## 【 학교 】 ##############################################


xmlUrl = 'https://open.neis.go.kr/hub/mealServiceDietInfo' #인터넷 주소
Key = '2f07e165bb1b4f38907826ef37478988' #키

def get_day(y,m,d):
    daylist = ['월', '화', '수', '목', '금', '토', '일']
    return daylist[datetime.date(y,m,d).weekday()]

def meal_daydata(MealDay):
    information = '?' + urlencode(
        {
            quote_plus('KEY') : Key,
            quote_plus('ATPT_OFCDC_SC_CODE') : "K10", # 강원도 교육청 
            quote_plus('SD_SCHUL_CODE') : "7004207", # 강원사대부고 번호
            quote_plus('MLSV_YMD') : MealDay,
            quote_plus('Type') : 'json'
        }
    )
    question = xmlUrl + information
    raw = requests.get(question).text
    return raw

Allergy = "1.난류 2.우유 3.메밀 4.땅콩 5.대두 6.밀 7.고등어 8.게 9.새우 10.돼지고기 11.복숭아 12.토마토 13.아황산류 14.호두 15.닭고기 16.쇠고기 17.오징어 18.조개류(굴, 전복, 홍합 포함)"
@bot.command()
async def 급식(ctx,*,date=None):
    if date == None:
        await ctx.send("급식 정보를 알고싶으시다면 → \"/급식 어제\",\"/급식 오늘\",\"/급식 내일\" 또는 \"/급식 <날짜>\"로 검색해주세요.\n`날짜로 검색 예시 : /급식 20220131`")
        return
    if date == "오늘":
        today = get_day(int(KRtime[:4]),int(KRtime[5:7]),int(KRtime[8:10]))
        embed = discord.Embed(title=f"SDHS 급식 ({KRtime[5:7]}월 {KRtime[8:10]}일 {today}요일)", color=0x62c1cc) # Embed의 기본 틀(색상, 메인 제목, 설명)을 잡아줍니다
        MealDay = f"{KRtime[:4]}{KRtime[5:7]}{KRtime[8:10]}"
        MealInfo = json.loads(meal_daydata(MealDay)) # 집합
        if list(MealInfo.keys())[0] == 'RESULT':
            embed.add_field(name="정보", value="당일 급식 메뉴가 존재하지 않거나, 아직 공개되지 않았습니다.", inline=False)
            await ctx.send(embed=embed)
            return
        MealName = (MealInfo['mealServiceDietInfo'][1]['row'][0]['DDISH_NM'])
        MealName = MealName.split('<br/>')
        MealName = '\n'.join(str(s) for s in MealName)
        MealKcal = (MealInfo['mealServiceDietInfo'][1]['row'][0]['CAL_INFO'])
        embed.add_field(name="메뉴", value=f"`{MealName}`", inline=False)
        embed.add_field(name="칼로리", value=f"`{MealKcal}`", inline=False)
        embed.add_field(name="알레르기", value=f"`{Allergy}`", inline=False)
        await ctx.send(embed=embed)
    elif date == "어제":
        if int(KRtime[8:10]) == 1:
            if (int(KRtime[5:7])-1) == 0:
                today = get_day(int(KRtime[:4]-1),12,31)
                embed = discord.Embed(title=f"SDHS 급식 (12월 31일 {today}요일)", color=0x62c1cc) # Embed의 기본 틀(색상, 메인 제목, 설명)을 잡아줍니다
                MealDay = f"{int(KRtime[:4])-1:04d}1231"
            elif (int(KRtime[5:7])-1) == 2 and int(KRtime[:4])%4 == 0:
                today = get_day(int(KRtime[:4]),2,29)
                embed = discord.Embed(title=f"SDHS 급식 (02월 29일 {today}요일)", color=0x62c1cc) # Embed의 기본 틀(색상, 메인 제목, 설명)을 잡아줍니다
                MealDay = f"{KRtime[:4]}0229"
            elif (int(KRtime[5:7])-1) == 2 and int(KRtime[:4])%4 != 0:
                today = get_day(int(KRtime[:4]),2,28)
                embed = discord.Embed(title=f"SDHS 급식 (02월 28일 {today}요일)", color=0x62c1cc) # Embed의 기본 틀(색상, 메인 제목, 설명)을 잡아줍니다
                MealDay = f"{KRtime[:4]}0228"
            elif (int(KRtime[5:7])-1) in [1,3,5,7,8,10]:
                today = get_day(int(KRtime[:4]),int(KRtime[5:7])-1,31)
                embed = discord.Embed(title=f"SDHS 급식 ({int(KRtime[5:7])-1:02d}월 31일 {today}요일)", color=0x62c1cc) # Embed의 기본 틀(색상, 메인 제목, 설명)을 잡아줍니다
                MealDay = f"{KRtime[:4]}{int(KRtime[5:7])-1:02d}31"
            elif (int(KRtime[5:7])-1) in [4,6,9,11]:
                today = get_day(int(KRtime[:4]),int(KRtime[5:7])-1,30)
                embed = discord.Embed(title=f"SDHS 급식 ({int(KRtime[5:7])-1:02d}월 30일 {today}요일)", color=0x62c1cc) # Embed의 기본 틀(색상, 메인 제목, 설명)을 잡아줍니다
                MealDay = f"{KRtime[:4]}{int(KRtime[5:7])-1:02d}30"
            MealInfo = json.loads(meal_daydata(MealDay)) # 집합
            if list(MealInfo.keys())[0] == 'RESULT':
                embed.add_field(name="정보", value="당일 급식 메뉴가 존재하지 않거나, 아직 공개되지 않았습니다.", inline=False)
                await ctx.send(embed=embed)
                return
            MealName = (MealInfo['mealServiceDietInfo'][1]['row'][0]['DDISH_NM'])
            MealName = MealName.split('<br/>')
            MealName = '\n'.join(str(s) for s in MealName)
            MealKcal = (MealInfo['mealServiceDietInfo'][1]['row'][0]['CAL_INFO'])
            embed.add_field(name="메뉴", value=f"`{MealName}`", inline=False)
            embed.add_field(name="칼로리", value=f"`{MealKcal}`", inline=False)
            embed.add_field(name="알레르기", value=f"`{Allergy}`", inline=False)
            await ctx.send(embed=embed)
        else:
            today = get_day(int(KRtime[:4]),int(KRtime[5:7]),(int(KRtime[8:10])-1))
            embed = discord.Embed(title=f"SDHS 급식 ({KRtime[5:7]}월 {int(KRtime[8:10])-1:02d}일 {today}요일)", color=0x62c1cc) # Embed의 기본 틀(색상, 메인 제목, 설명)을 잡아줍니다
            MealDay = f"{KRtime[:4]}{KRtime[5:7]}{int(KRtime[8:10])-1:02d}"
            MealInfo = json.loads(meal_daydata(MealDay)) # 집합
            if list(MealInfo.keys())[0] == 'RESULT':
                embed.add_field(name="정보", value="당일 급식 메뉴가 존재하지 않거나, 아직 공개되지 않았습니다.", inline=False)
                await ctx.send(embed=embed)
                return
            MealName = (MealInfo['mealServiceDietInfo'][1]['row'][0]['DDISH_NM'])
            MealName = MealName.split('<br/>')
            MealName = '\n'.join(str(s) for s in MealName)
            MealKcal = (MealInfo['mealServiceDietInfo'][1]['row'][0]['CAL_INFO'])
            embed.add_field(name="메뉴", value=f"`{MealName}`", inline=False)
            embed.add_field(name="칼로리", value=f"`{MealKcal}`", inline=False)
            embed.add_field(name="알레르기", value=f"`{Allergy}`", inline=False)
            await ctx.send(embed=embed)
    elif date == "내일":
        if int(KRtime[8:10]) == 31 and int(KRtime[5:7]) == 12:
            today = get_day(int(KRtime[:4]+1),1,1)
            embed = discord.Embed(title=f"SDHS 급식 (01월 01일 {today}요일)", color=0x62c1cc) # Embed의 기본 틀(색상, 메인 제목, 설명)을 잡아줍니다
            MealDay = f"{int(KRtime[:4])+1:04d}0101"
        elif int(KRtime[8:10]) == 29 and int(KRtime[5:7]) == 2 and int(KRtime[:4])%4 == 0:
            today = get_day(int(KRtime[:4]),int(KRtime[5:7])+1,1)
            embed = discord.Embed(title=f"SDHS 급식 ({int(KRtime[5:7])+1:02d}월 01일 {today}요일)", color=0x62c1cc) # Embed의 기본 틀(색상, 메인 제목, 설명)을 잡아줍니다
            MealDay = f"{KRtime[:4]}{int(KRtime[5:7])+1:02d}01"
        elif int(KRtime[8:10]) == 28 and int(KRtime[5:7]) == 2 and int(KRtime[:4])%4 != 0:
            today = get_day(int(KRtime[:4]),int(KRtime[5:7])+1,1)
            embed = discord.Embed(title=f"SDHS 급식 ({int(KRtime[5:7])+1:02d}월 01일 {today}요일)", color=0x62c1cc) # Embed의 기본 틀(색상, 메인 제목, 설명)을 잡아줍니다
            MealDay = f"{KRtime[:4]}{int(KRtime[5:7])+1:02d}01"
        elif int(KRtime[8:10]) == 31 and int(KRtime[5:7]) in [1,3,5,7,8,10]:
            today = get_day(int(KRtime[:4]),int(KRtime[5:7])+1,1)
            embed = discord.Embed(title=f"SDHS 급식 ({int(KRtime[5:7])+1:02d}월 01일 {today}요일)", color=0x62c1cc) # Embed의 기본 틀(색상, 메인 제목, 설명)을 잡아줍니다
            MealDay = f"{KRtime[:4]}{int(KRtime[5:7])+1:02d}01"
        elif int(KRtime[8:10]) == 30 and int(KRtime[5:7]) in [4,6,9,11]:
            today = get_day(int(KRtime[:4]),int(KRtime[5:7])+1,1)
            embed = discord.Embed(title=f"SDHS 급식 ({int(KRtime[5:7])+1:02d}월 01일 {today}요일)", color=0x62c1cc) # Embed의 기본 틀(색상, 메인 제목, 설명)을 잡아줍니다
            MealDay = f"{KRtime[:4]}{int(KRtime[5:7])+1:02d}01"
            MealInfo = json.loads(meal_daydata(MealDay)) # 집합
        else:
            today = get_day(int(KRtime[:4]),int(KRtime[5:7]),int(KRtime[8:10])+1)
            embed = discord.Embed(title=f"SDHS 급식 ({KRtime[5:7]}월 {int(KRtime[8:10])+1:02d}일 {today}요일)", color=0x62c1cc) # Embed의 기본 틀(색상, 메인 제목, 설명)을 잡아줍니다
            MealDay = f"{KRtime[:4]}{KRtime[5:7]}{int(KRtime[8:10])+1:02d}"
        MealInfo = json.loads(meal_daydata(MealDay)) # 집합
        if list(MealInfo.keys())[0] == 'RESULT':
            embed.add_field(name="정보", value="당일 급식 메뉴가 존재하지 않거나, 아직 공개되지 않았습니다.", inline=False)
            await ctx.send(embed=embed)
            return
        MealName = (MealInfo['mealServiceDietInfo'][1]['row'][0]['DDISH_NM'])
        MealName = MealName.split('<br/>')
        MealName = '\n'.join(str(s) for s in MealName)
        MealKcal = (MealInfo['mealServiceDietInfo'][1]['row'][0]['CAL_INFO'])
        embed.add_field(name="메뉴", value=f"`{MealName}`", inline=False)
        embed.add_field(name="칼로리", value=f"`{MealKcal}`", inline=False)
        embed.add_field(name="알레르기", value=f"`{Allergy}`", inline=False)
        await ctx.send(embed=embed)
    else:
        if len(date) == 8:
            today = get_day(int(date[:4]),int(date[4:6]),int(date[6:8]))
            embed = discord.Embed(title=f"SDHS 급식 ({date[4:6]}월 {date[6:8]}일 {today}요일)", color=0x62c1cc)
            MealDay = date
            MealInfo = json.loads(meal_daydata(MealDay)) # 집합
            if list(MealInfo.keys())[0] == 'RESULT':
                embed.add_field(name="정보", value="당일 급식 메뉴가 존재하지 않거나, 아직 공개되지 않았습니다.", inline=False)
                await ctx.send(embed=embed)
                return
            MealName = (MealInfo['mealServiceDietInfo'][1]['row'][0]['DDISH_NM'])
            MealName = MealName.split('<br/>')
            MealName = '\n'.join(str(s) for s in MealName)
            MealKcal = (MealInfo['mealServiceDietInfo'][1]['row'][0]['CAL_INFO'])
            embed.add_field(name="메뉴", value=f"`{MealName}`", inline=False)
            embed.add_field(name="칼로리", value=f"`{MealKcal}`", inline=False)
            embed.add_field(name="알레르기", value=f"`{Allergy}`", inline=False)
            await ctx.send(embed=embed)
        else:
            await ctx.send("다시 입력해주세요.")

@bot.command()
async def 시간표(ctx):
    await ctx.send("구현중입니다.")

@bot.command()
async def 학사일정(ctx):
    embed = discord.Embed(title="학사일정 [2022년 1학기]", color=0x62c1cc) # Embed의 기본 틀(색상, 메인 제목, 설명)을 잡아줍니다
    embed.set_image(url="https://media.discordapp.net/attachments/995202193185591297/1036536068062855238/unknown.png?width=524&height=630")
    await ctx.send(embed=embed)
    await asyncio.sleep(2)
    embed = discord.Embed(title="학사일정 [2022년 2학기]", color=0x62c1cc) # Embed의 기본 틀(색상, 메인 제목, 설명)을 잡아줍니다
    embed.set_image(url="https://media.discordapp.net/attachments/995202193185591297/1036536172727504967/unknown.png?width=554&height=630")
    await ctx.send(embed=embed)

############################################## 【 시스템 】 ##############################################


@bot.command() 
async def 정보(ctx):
    await ctx.send('봇 정보 : 구동 체제 - VScode (Python) 버전 : 3.10.8 *기반 : project POPPY (discord.py : 2.0.1')

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
bot.run(TOKEN)
