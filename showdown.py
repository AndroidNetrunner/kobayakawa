from start_round import start_round
import discord

async def showdown(current_game, current_round):
    lowest = judge_who_gets_support(current_round)
    embed = discord.Embed(title="모든 플레이어가 베팅을 끝냈습니다.")
    pot = len(current_round.caller) + 1 if current_game.current_round != 6 else len(current_round.caller) * 2 + 2
    if len(current_round.caller) == 0:
        embed.add_field(name="베팅에 참여한 플레이어가 존재하지 않습니다.", value="이번 라운드는 승자 없이 종료됩니다.")
    elif len(current_round.caller) == 1:
        winner = current_round.caller[0]
        embed.add_field(name=f"베팅에 참여한 플레이어가 {winner.name}님뿐입니다.",value=f"{winner.name}님이 칩을 획득하고, 카드는 공개되지 않습니다.")
        current_game.chips[winner] += pot
    else:
        str_players_and_cards = ""
        for caller in current_round.caller:
            str_players_and_cards += f"{caller.name} : {current_round.hand[caller]}\n"
        embed.add_field(name="베팅에 참여한 플레이어들과 카드는 다음과 같습니다.", value=str_players_and_cards, inline=False)
        current_round.hand[lowest] += current_round.support_card
        str_players_and_cards = ""
        for caller in current_round.caller:
            str_players_and_cards += f"{caller.name} : {current_round.hand[caller]}\n"
        embed.add_field(name=f"가장 낮은 카드를 가진 {lowest.name}님은 코바야카와 카드({current_round.support_card})를 지원받고, 그에 따른 결과는 다음과 같습니다.", value=str_players_and_cards, inline=False)
        winner = judge_who_is_winner(current_round)
        embed.add_field(name=f"이번 라운드의 승자는 {winner.name}님입니다!", value=f"{winner.name}님은 {pot}개의 칩을 획득하셨습니다.")
        current_game.chips[winner] += pot
    await current_game.main_channel.send(embed=embed)
    current_game.current_round += 1
    current_game.index_of_first_player = (current_game.index_of_first_player + 1) % len(current_game.members)
    await start_round(current_game)
    
def judge_who_gets_support(current_round):
    lowest = None
    for caller in current_round.caller:
        if not lowest or current_round.hand[caller] < current_round.hand[lowest]:
            lowest = caller
    return lowest

def judge_who_is_winner(current_round):
    winner = None
    for caller in current_round.caller:
        if not winner or current_round.hand[caller] > current_round.hand[winner]:
            winner = caller
    return winner