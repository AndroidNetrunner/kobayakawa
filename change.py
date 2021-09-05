import discord

async def change_hand(current_round):
    current_round.temp_card = current_round.deck.pop()
    embed = discord.Embed(title = f"손패 바꾸기를 선택하셨습니다.", description= f"당신이 덱에서 뽑은 카드는 {current_round.temp_card}입니다.")
    embed.add_field(name="손에 있는 카드를 새로 뽑은 카드로 바꿀까요?", value="카드를 바꾸려면 ⭕를, 카드를 바꾸지 않으려면 ❌를 눌러주세요!")
    message = await current_round.turn.send(embed=embed)
    await message.add_reaction("⭕")
    await message.add_reaction("❌")

async def change_support_card(current_round):
    current_round.support_card = current_round.deck.pop()
    embed = discord.Embed(title = f"코바야카와 카드 바꾸기를 선택하셨습니다.", description=f"새로 뽑은 코바야카와 카드는 {current_round.support_card}입니다.")
    await current_round.turn.send(embed=embed)