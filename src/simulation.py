from src.player import Player


class Simulation:
    def __init__(self, grid, players, starting_positions=None):
        self.grid = grid
        self.players = []
        if starting_positions:
            for i, (row, col) in enumerate(starting_positions):
                self.players.append(Player(f"Player {i + 1}", row, col, (i * 50, i * 10, 255 - i * 50)))
        else:
            for i in range(players):
                self.players.append(Player(f"Player {i + 1}", 0, 0, (255, 100, 100)))
        self.met = False
        self.winner_message = ""

    def reset(self):
        for player in self.players:
            player.reset()
        self.met = False
        self.winner_message = ""