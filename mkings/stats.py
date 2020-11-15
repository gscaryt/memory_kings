from datetime import datetime
from .players import Player
from .cards import Card


class Stats:
    def __init__(self):
        self.start_time = None
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
        self.end_time = None
        self.abandoned = None
        self.queen_uses = None
        
    def collect_start_data(self,game):
        self.start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.num_of_players = game._num_of_players-1
        self.grid_size = game._grid_size
        self.setup_variant = game._setup_variant

    def collect_end_data(self,game):
        self.turns = game._turns
        if game._winner is not None:
            self.winner = f'Player {game._winner.order}'
        if len(Player.array[0].pawn) != 0:
            self.counter_position = (Player.array[0].pawn[0].col+1, Player.array[0].pawn[0].row+1)
            self.counter_score = Player.array[0].score
        self.player1_score = Player.array[1].score
        if self.num_of_players > 1:
            self.player2_score = Player.array[2].score
        if self.num_of_players > 2:
            self.player3_score = Player.array[3].score
        if self.num_of_players > 3:
            self.player4_score = Player.array[4].score
        self.end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.abandoned = game._abandoned
        self.queen_uses = Card.queen_uses

    def build_dict(self):
        return {
            "Start Time": self.start_time,
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
            "End Time": self.end_time,
            "Abandoned": self.abandoned,
            "Queen Uses": self.queen_uses,
            }

    def write_data(self):
        game_stats = self.build_dict()
        values = list(game_stats.values())
        with open('docs/mkings_data.txt', 'a') as data_file:
            for data in values:
                data_file.write(f'{data}; ')
            data_file.write('\n')
