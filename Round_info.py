import random

class Round_info:
    def __init__(self, game_room):
        self.deck = self.shuffle_deck()
        self.hand = {}
        self.support_card = self.deck.pop()
        self.survivors = self.judge_survivors(game_room)
        self.first_player = self.set_first_player(game_room)
        self.turn = self.first_player
        self.temp_card = None
        self.caller = []
        self.main_channel = game_room.main_channel
        
    def shuffle_deck(self):
        deck = list(range(1,16))
        random.shuffle(deck)
        return deck

    def judge_survivors(self, game_room):
        survivors = []
        for player in game_room.members:
            if game_room.chips[player] > 0:
                survivors.append(player)
        return survivors

    def deal_cards(self):
        for survivor in self.survivors:
            self.hand[survivor] = self.deck.pop()
    
    def set_first_player(self, game_room):
        first_player = game_room.members[game_room.index_of_first_player]
        game_room.index_of_first_player = (game_room.index_of_first_player + 1) % len(game_room.members)
        while game_room.members[game_room.index_of_first_player] not in self.survivors:
            game_room.index_of_first_player = (game_room.index_of_first_player + 1) % len(game_room.members)
        return first_player
        
    def next_turn(self):
        if self.turn in self.survivors:
            index = self.survivors.index(self.turn)
            self.turn = self.survivors[(index + 1) % len(self.survivors)]
        else:
            index = self.members.index(self.turn)
            self.turn = self.members[(index + 1) % len(self.members)]
            while self.turn not in self.survivors:
                index = (index + 1) % len(self.members)
                self.turn = self.members[(index + 1) % len(self.members)]