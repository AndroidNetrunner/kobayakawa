import discord
from game_data import active_game

async def end_game(game_room):
    game_result = ""
    for player in game_room.members:
        game_result += f"{player.name} : {game_room.chips[player]}\n"
    embed = discord.Embed(title="게임이 모두 종료되었습니다.", description=f"각 플레이어들의 보유 칩은 다음과 같습니다.\n{game_result}")
    winner = declare_winner(game_room)
    embed.add_field(name="게임 결과, 우승자는...", value=f"{' '.join(winner)}입니다!")
    await game_room.main_channel.send(embed=embed)
    del active_game[game_room.main_channel.channel.id]

def declare_winner(game_room):
    winner = []
    winner_name = []
    for player in game_room.members:
        if (not winner) or game_room.chips[winner[0]] < game_room.chips[player]:
            winner = [player]
        elif game_room.chips[winner[0]] == game_room.chips[player]:
            winner.append(player)
    for player in winner:
        winner_name.append(player.name)
    return winner_name

async def end_game_early(game_room, current_round):
    sole_survivor = current_round.survivors[0]
    embed = discord.Embed(title="게임이 조기 종료되었습니다.", description=f"{sole_survivor.name}님이 칩을 모두 획득하셨습니다!")
    await game_room.main_channel.send(embed=embed)
    del active_game[game_room.main_channel.channel.id]