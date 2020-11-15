class Stats:
    def __init__(self):
        self.num_of_players = None
        self.grid_size = None
        self.setup_variant = None
        self.turns = None
        self.winner = None
        self.counter_position = None
        self.counter_score = None
        self.player1_score = None
        self.player2_score = None
        self.player3_score = None
        self.player4_score = None
        self.time = None
        self.abandoned = None
    
    def build_dict(self):
        return = {
            "Players": self.num_of_players,
            "Grid": self.grid_size,
            "Setup": self.setup_variant,
            "Turns": self.turns,
            "Winner": self.winner,
            "Counter Position": self.counter_position,
            "Score Counter": self.counter_score,
            "Score Player 1": self.player1_score,
            "Score Player 2": self.player2_score,
            "Score Player 3": self.player3_score,
            "Score Player 4": self.player4_score,
            "Game Duration": self.time,
            "Abandoned": self.abandoned,
            }

    def write_data(self)
        game_stats = self.build_dict()
        with open('mkings_data.txt', 'w') as data_file:
        # Write all Rounds Data
            data_file.write('[Players, Grid, Setup, Turns, Winner, CounterPos, Counter, Player1, Player2, Player3, Player4, Duration, Abandoned]\n')
            for dictionary in game_stats:
                data_file.write(f'{list(dictionary.values())}\n')