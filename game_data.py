class Game_data:
    def __init__(self):
        self.members = []
        self.chips = {}
        self.current_round = 0
        self.first_player = None
        self.round_info = None
        self.can_join = False
        self.start = False
        self.main_channel = None
        
active_game = {}