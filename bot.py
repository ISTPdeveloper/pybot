import asyncio, discord, os
from discord.ext import commands
from dotenv import load_dotenv

from src.lunch_menu import *
from embed.help_embed import *
from game.dice import *
from src.user import *
from fuck import *
import random

load_dotenv()

TOKEN = os.getenv("TOKEN")

PREFIX = os.getenv("PREFIX")

ADMIN_ID = os.getenv("ADMIN_ID")

# 봇 동작 명령어
bot = commands.Bot(command_prefix='응애 ', help_command = None)
client = discord.Client()

# 준비 확인
@bot.event
async def on_ready():
    print("다음으로 로그인합니다 : {0.user}".format(bot))
    await bot.change_presence(status=discord.Status.online, activity=None)

# 도움말 출력 명령어
@bot.command(aliases=['help', '명령어', '?'])
async def 도움말(ctx) :
    await ctx.send(embed=help_embed)
         
@bot.command(aliases=['안녕', '안녕하세요', 'ㅎㅇ'])
async def hello(ctx):
    await ctx.send("안녕하세요")
    
# 핑 출력 명령어    
@bot.command(aliases=['ping', 'PING', 'Ping'])
async def 핑(ctx):
    await ctx.send(f"현재 핑은 `{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}` 기준으로 `{str(round(bot.latency*1000))}ms` 입니다.")
# 날짜 출력 명령어
@bot.command(aliases=['date', 'DATE', 'Date'])
async def 날짜(ctx):
    await ctx.send(f"{datetime.datetime.now().strftime('%Y. %m. %d')}")
# 시간 출력 명령어
@bot.command(aliases=['time', 'TIME', 'Time'])
async def 시간(ctx):
    await ctx.send(f"{datetime.datetime.now().strftime('%H:%M:%S')}")
# 점심 메뉴 출력 명령어 
@bot.command(aliases=['밥', '메뉴', '점심', '급식', 'lunch', 'Lunch', 'LUNCH', 'menu'])
async def 밥줘(ctx, day=None,user: discord.User=None):
    if day == None:
        day = str(datetime.datetime.now().strftime('%Y%m%d'))
    if user==None:
        user = str(ctx.author.id)
    else:
        user = str(user.id)
    if len(day) == 8 and day.isdigit():
        embed = discord.Embed(title="급식 정보", description=f"일시 : `{day}`", color=0xffb266)
        msg = element

        embed.add_field(name="급식",value=f">>> {msg}", inline=False)
        await ctx.send(embed=embed)   
        
# 주사위 게임 명령어    
@bot.command()
async def 주사위(ctx):
    userExistance, userRow = checkUser(ctx.author.name, ctx.author.id)
    if userExistance:
        print("DB에서 ", ctx.author.name, "을 찾았습니다.")
        cur_money = getMoney(ctx.author.name, userRow)
    def dice():
        a = random.randrange(1,7)
        b = random.randrange(1,7)
        if a > b:
            betting = cur_money
            modifyMoney(ctx.author.name, userRow, -int(5000))
            return "패배", 0xFF0000, str(a), str(b)
        elif a == b:
            return "무승부", 0xFAFA00, str(a), str(b)
        elif a < b:
            betting = cur_money
            modifyMoney(ctx.author.name, userRow, int(5000))
            return "승리", 0x00ff56, str(a), str(b)
    
    result, _color, bot, user = dice()
    embed = discord.Embed(title = "주사위 게임", description = "결과", color = _color)
    embed.add_field(name = "응애 봇의 숫자", value = ":game_die: " + bot, inline = True)
    embed.add_field(name = ctx.author.name+"의 숫자", value = ":game_die: " + user, inline = True)
    embed.set_footer(text="결과: " + result)
    
    await ctx.send(embed=embed)

# 도박 명령어
@bot.command()
async def 도박(ctx, money):
    userExistance, userRow = checkUser(ctx.author.name, ctx.author.id)
    win = gamble()
    result = ""
    betting = 0
    _color = 0x000000
    if userExistance:
        print("DB에서 ", ctx.author.name, "을 찾았습니다.")
        cur_money = getMoney(ctx.author.name, userRow)

        if money == "올인":
            betting = cur_money
            if win:
                result = "성공"
                _color = 0x00ff56
                print(result)

                modifyMoney(ctx.author.name, userRow, int(1*betting))

            else:
                result = "실패"
                _color = 0xFF0000
                print(result)

                modifyMoney(ctx.author.name, userRow, -int(betting))
                addLoss(ctx.author.name, userRow, int(betting))

            embed = discord.Embed(title = ctx.author.name + "의 도박결과", description = result, color = _color)
            embed.add_field(name = "배팅금액", value = betting, inline = False)
            embed.add_field(name = "현재 자산", value = getMoney(ctx.author.name, userRow), inline = False)

            await ctx.send(embed=embed)
            
        elif int(money) >= 10:
            if cur_money >= int(money):
                betting = int(money)
                print("배팅금액: ", betting)
                print("")

                if win:
                    result = "성공"
                    _color = 0x00ff56
                    print(result)

                    modifyMoney(ctx.author.name, userRow, int(0.5*betting))

                else:
                    result = "실패"
                    _color = 0xFF0000
                    print(result)

                    modifyMoney(ctx.author.name, userRow, -int(betting))
                    addLoss(ctx.author.name, userRow, int(betting))

                embed = discord.Embed(title = ctx.author.name + "의 도박결과", description = result, color = _color)
                embed.add_field(name = "배팅금액", value = betting, inline = False)
                embed.add_field(name = "현재 자산", value = getMoney(ctx.author.name, userRow), inline = False)

                await ctx.send(embed=embed)

            else:
                print("돈이 부족합니다.")
                print("배팅금액: ", money, " | 현재자산: ", cur_money)
                await ctx.send("돈이 부족합니다. 현재자산: " + str(cur_money))
        else:
            print("배팅금액", money, "가 10보다 작습니다.")
            await ctx.send("10원 이상만 배팅 가능합니다.")
    else:
        print("DB에서 ", ctx.author.name, "을 찾을 수 없습니다")
        await ctx.send("도박은 회원가입 후 이용 가능합니다.")

    print("------------------------------\n")
# 랭킹 출력 명령어
@bot.command()
async def 랭킹(ctx):
    rank = ranking()
    embed = discord.Embed(title = "돈 보유", description = "순위", color = 0x4A44FF)

    for i in range(0,len(rank)):
        if i%2 == 0:
            name = rank[i]
            money = rank[i+1]
            embed.add_field(name = str(int(i/2+1))+"위 "+name, value ="돈 : "+str(money), inline=False)

    await ctx.send(embed=embed)
# 회원가입 명령어       
@bot.command()
async def 회원가입(ctx):
    print("회원가입이 가능한지 확인합니다.")
    userExistance, userRow = checkUser(ctx.author.name, ctx.author.id)
    if userExistance:
        print("DB에서 ", ctx.author.name, "을 찾았습니다.")
        print("------------------------------\n")
        await ctx.send("이미 가입하셨습니다.")
    else:
        print("DB에서 ", ctx.author.name, "을 찾을 수 없습니다")
        print("")

        Signup(ctx.author.name, ctx.author.id)

        print("회원가입이 완료되었습니다.")
        print("------------------------------\n")
        await ctx.send("회원가입이 완료되었습니다.")
# 탈퇴 명령어        
@bot.command()
async def 탈퇴(ctx):
    print("탈퇴가 가능한지 확인합니다.")
    userExistance, userRow = checkUser(ctx.author.name, ctx.author.id)
    if userExistance:
        DeleteAccount(userRow)
        print("탈퇴가 완료되었습니다.")
        print("------------------------------\n")

        await ctx.send("탈퇴가 완료되었습니다.")
    else:
        print("DB에서 ", ctx.author.name, "을 찾을 수 없습니다")
        print("------------------------------\n")

        await ctx.send("등록되지 않은 사용자입니다.")
# 내 정보 출력 명령어
@bot.command()
async def 내정보(ctx):
    userExistance, userRow = checkUser(ctx.author.name, ctx.author.id)

    if not userExistance:
        print("DB에서 ", ctx.author.name, "을 찾을 수 없습니다")
        print("------------------------------\n")
        await ctx.send("회원가입 후 자신의 정보를 확인할 수 있습니다.")
    else:
        money, loss = userInfo(userRow)
        rank = getRank(userRow)
        userNum = checkUserNum()
        print("------------------------------\n")
        
        embed = discord.Embed(title="유저 정보", description = ctx.author.name, color = 0x62D0F6)
        embed.add_field(name = "순위", value = str(rank) + "/" + str(userNum))
        embed.add_field(name = "보유 자산", value = money, inline = False)
        embed.add_field(name = "도박으로 날린 돈", value = loss, inline = False)
        await ctx.send(embed=embed)
        
#다른 사람 정보 출력 명령어
@bot.command()
async def 정보(ctx, user: discord.User):
    userExistance, userRow = checkUser(user.name, user.id)

    if not userExistance:
        print("DB에서 ", user.name, "을 찾을 수 없습니다")
        print("------------------------------\n")
        await ctx.send(user.name  + " 은(는) 등록되지 않은 사용자입니다.")
    else:
        money, loss = userInfo(userRow)
        rank = getRank(userRow)
        userNum = checkUserNum()
        print("------------------------------\n")
        embed = discord.Embed(title="유저 정보", description = user.name, color = 0x62D0F6)
        embed.add_field(name = "순위", value = str(rank) + "/" + str(userNum))
        embed.add_field(name = "보유 자산", value = money, inline = False)
        embed.add_field(name = "도박으로 날린 돈", value = loss, inline = False)
        await ctx.send(embed=embed)
        
# 송금 명령어
@bot.command()
async def 송금(ctx, user: discord.User, money):
    print("송금이 가능한지 확인합니다.")
    senderExistance, senderRow = checkUser(ctx.author.name, ctx.author.id)
    receiverExistance, receiverRow = checkUser(user.name, user.id)

    if not senderExistance:
        print("DB에서", ctx.author.name, "을 찾을수 없습니다")
        print("------------------------------\n")
        await ctx.send("회원가입 후 송금이 가능합니다.")
    elif not receiverExistance:
        print("DB에서 ", user.name, "을 찾을 수 없습니다")
        print("------------------------------\n")
        await ctx.send(user.name  + " 은(는) 등록되지 않은 사용자입니다.")
    else:
        print("송금하려는 돈: ", money)

        s_money = getMoney(ctx.author.name, senderRow)
        r_money = getMoney(user.name, receiverRow)

        if s_money >= int(money) and int(money) != 0:
            print("돈이 충분하므로 송금을 진행합니다.")
            print("")

            remit(ctx.author.name, senderRow, user.name, receiverRow, money)

            print("송금이 완료되었습니다. 결과를 전송합니다.")

            embed = discord.Embed(title="송금 완료", description = "송금된 돈: " + money, color = 0x77ff00)
            embed.add_field(name = "보낸 사람: " + ctx.author.name, value = "현재 자산: " + str(getMoney(ctx.author.name, senderRow)))
            embed.add_field(name = "→", value = ":moneybag:")
            embed.add_field(name="받은 사람: " + user.name, value="현재 자산: " + str(getMoney(user.name, receiverRow)))
                    
            await ctx.send(embed=embed)
        elif int(money) == 0:
            await ctx.send("0원을 보낼 필요는 없죠")
        else:
            print("돈이 충분하지 않습니다.")
            print("송금하려는 돈: ", money)
            print("현재 자산: ", s_money)
            await ctx.send("돈이 충분하지 않습니다. 현재 자산: " + str(s_money))

        print("------------------------------\n")
        
@bot.command(aliases=["add", "추가", "돈추가"])
async def 돈(ctx, money):
    
        if str(ctx.author.id) != ADMIN_ID:
            await ctx.send("관리자 권한이 없어 해당 명령어를 사용할 수 없습니다.")
        else:
            user, row = checkUser(ctx.author.name, ctx.author.id)
            addMoney(row, int(money))
            print("money")
        
@bot.command(aliases=["초기화"])
async def reset(ctx):
    if str(ctx.author.id) != ADMIN_ID:
        await ctx.send("관리자 권한이 없어 해당 명령어를 사용할 수 없습니다.")
    else:
        resetData()

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
    	await ctx.send("명령어를 찾지 못했습니다")
               
# Token 값을 통해 로그인하고 봇을 실행
bot.run(TOKEN)
