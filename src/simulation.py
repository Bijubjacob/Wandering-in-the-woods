from player import Player


class Simulation:
    def __init__(self, grid):
        self.grid = grid
        self.players = [
            Player("Player 1", 0, 0, (255, 100, 100)),
            Player("Player 2", grid.rows - 1, grid.cols - 1, (100, 100, 255)),
        ]
        self.met = False
        self.winner_message = ""

    def reset(self):
        for player in self.players:
            player.reset()
        self.met = False
        self.winner_message = ""