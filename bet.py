import discord

async def start_bet(current_round):
    embed = discord.Embed(title=f"이제 베팅을 결정하실 차례입니다!",description=f"손패의 카드는 {current_round.hand[current_round.turn]}이며, 코바야카와 카드는 {current_round.support_card}입니다.")
    embed.add_field(name="본인의 카드를 교체하고 싶다면,", value=f":regional_indicator_o:를 눌러주세요! 새로운 카드가 지급된 후, 본인의 카드를 결정하시면 됩니다.", inline=False)
    embed.add_field(name="코바야카와 카드를 교체하고 싶다면,", value=f":regional_indicator_x:을 눌러주세요! 코바야카와 카드가 바뀐 후 모두에게 공유됩니다.")
    message = await current_round.turn.send(embed=embed)
    await message.add_reaction("🇴")
    await message.add_reaction("🇽")