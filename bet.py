import discord
from showdown import showdown

async def start_bet(current_round):
    embed = discord.Embed(title=f"이제 베팅을 결정하실 차례입니다!",description=f"손패의 카드는 {current_round.hand[current_round.turn]}이며, 코바야카와 카드는 {current_round.support_card}입니다.")
    embed.add_field(name="베팅에 참여하고 싶다면,", value=f"🅾️를 눌러주세요! 베팅을 위해서는 칩 1개가 소모됩니다.", inline=False)
    embed.add_field(name="베팅에 참여하고 싶지 않다면,", value=f"❎을 눌러주세요! 이번 라운드에는 더 이상 참여하실 수 없습니다.")
    message = await current_round.turn.send(embed=embed)
    await message.add_reaction("🅾️")
    await message.add_reaction("❎")

async def call(current_game, current_round):
    current_round.caller.append(current_round.turn)
    await current_round.turn.send("베팅에 참여하기를 선택하셨습니다.")
    current_game.chips[current_round.turn] -= 1 if current_game.current_round != 6 else 2
    current_round.next_turn()
    if current_round.turn != current_round.first_player:
        await start_bet(current_round)
    else:
        await showdown(current_game, current_round)

async def fold(current_game, current_round):
    await current_round.turn.send("베팅에 참여하지 않기를 선택하셨습니다.")
    current_round.next_turn()
    if current_round.turn != current_round.first_player:
        await start_bet(current_round)
    else:
        await showdown(current_game, current_round)