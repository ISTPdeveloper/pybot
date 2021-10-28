import discord

end_msg = "\n\n개발자 : 김대욱#1859 | [개발자 서버](https://discord.gg/g4b2BWNhNJ) | [초대링크](https://discord.com/api/oauth2/authorize?client_id=892590924046159903&permissions=8&scope=bot)"

help_embed = discord.Embed(title="명령어", description="응애 봇에 대한 도움말 입니다. 응애 명령어 로 확인 가능합니다.", color=0x62c1cc)
help_embed.add_field(name="응애 밥줘", value="```응애 봇이 당일 급식 메뉴를 알려줍니다.```" , inline=False)
help_embed.add_field(name ="응애 회원가입", value = "```각종 컨텐츠를 즐기기 위한 회원가입을 합니다```", inline = False)
help_embed.add_field(name ="응애 탈퇴", value = "```탈퇴를 진행합니다```", inline=False)
help_embed.add_field(name ="응애 내정보", value = "```유저의 순위, 보유자산, 도박으로 날린 돈 등을 확인 가능합니다.```", inline=False)
help_embed.add_field(name ="응애 정보 [대상]", value = "```멘션한 [대상]의 정보를 확인합니다```", inline=False)
help_embed.add_field(name ="응애 도박", value = "```도박을 하여 돈을 불릴 수 있습니다.```", inline=False)
help_embed.add_field(name ="응애 주사위", value = "```주사위를 굴려 봇과 대결합니다.```", inline=False)
help_embed.add_field(name= "응애 기타 명령어", value="```응애 날짜, 응애 시간, 응애 핑, 응애 안녕 등의 명령어 사용이 가능합니다.```" , inline=False)
help_embed.add_field(name="정보",value=end_msg)