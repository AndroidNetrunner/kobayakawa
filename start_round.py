from Round_info import Round_info
from end_game import end_game, end_game_early
import random
import discord

async def start_round(game_room):
    if game_room.current_round > 6:
        await end_game(game_room)
        return
    current_round = Round_info(game_room)
    if len(current_round.survivors) == 1:
        await end_game_early(game_room, current_round)
        return
    game_room.round_info = current_round
    current_round.deal_cards()
    for survivor in current_round.survivors:
        embed = discord.Embed(title=f"{game_room.current_round + 1}라운드가 시작되었습니다!", description=f"당신의 카드는 {current_round.hand[survivor]}이며, 코바야카와 카드는 {current_round.support_card}입니다.")
        await survivor.send(embed=embed)
    if current_round.turn not in current_round.survivors:
        current_round.next_turn()
    await current_round.main_channel.send(f"{game_room.current_round + 1}라운드가 시작되었습니다!\n선 플레이어는 {current_round.first_player.name}입니다.")
    await notify_turn(current_round)
    
async def notify_turn(current_round):
    embed = discord.Embed(title=f"이제 당신의 차례입니다!",description=f"본인의 카드를 교체하거나, 코바야카와 카드(현재 숫자: {current_round.support_card})를 교체할 수 있습니다.")
    embed.add_field(name="본인의 카드를 교체하고 싶다면,", value=f"0\u20E3을 눌러주세요! 새로운 카드가 지급된 후, 본인의 카드를 결정하시면 됩니다.", inline=False)
    embed.add_field(name="코바야카와 카드를 교체하고 싶다면,", value=f"1\u20E3을 눌러주세요! 코바야카와 카드가 바뀐 후 모두에게 공유됩니다.")
    message = await current_round.turn.send(embed=embed)
    await message.add_reaction("0\u20E3")
    await message.add_reaction("1\u20E3")