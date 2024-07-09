xmlUrl = 'https://open.neis.go.kr/hub/mealServiceDietInfo' #인터넷 주소
Key = '2f07e165bb1b4f38907826ef37478988' #키

NMJ = False # 내맘점 운영기간

# 내 맘대로 점심
@bot.command(aliases=['내맘대로점심','ㄴㅁㅈ'])
async def 내맘점(ctx):
    KRtime = datetime.datetime.now(pytz.timezone('Asia/Seoul')).strftime('%Y-%m-%d-%p-%I-%M-%S') #UTC+9
    if NMJ == True:
        await ctx.send(f"현재 {KRtime[5:7]}월 강원사대부고 내 마음대로 점심이 운영중이에요.")
        await ctx.send("n월n일까지 신청할 수 있습니다.")
        embed = discord.Embed(title="내맘점 신청",description='[링크](https://m.site.naver.com/qrcode/view.naver?v=12pq8) 에서 신청할 수 있습니다.', color=0x62c1cc)
        embed.set_image(url="https://media.discordapp.net/attachments/1034286732713132032/1036859140556988456/IMG_6958.jpg?width=473&height=631")
        await ctx.send(embed=embed)
    else:
        await ctx.send("현재 강원사대부고 내 맘대로 점심을 운영하고 있지 않아요. 다음에 다시 신청해주세요 :)")

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
    KRtime = datetime.datetime.now(pytz.timezone('Asia/Seoul')).strftime('%Y-%m-%d-%p-%I-%M-%S') #UTC+9
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