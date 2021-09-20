import random

def ready_game(game_room):
    for player in game_room.members:
        game_room.chips[player] = 4
    game_room.index_of_first_player = random.randrange(len(game_room.members))