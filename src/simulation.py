from src.player import Player

ANIMAL_TYPES = ["rabbit", "fox", "owl", "raccoon"]
ANIMAL_NAMES = ["Rabbit", "Fox", "Owl", "Raccoon"]


class Simulation:
    def __init__(self, grid, players, starting_positions=None):
        self.grid = grid
        self.players = []
        if starting_positions:
            for i, (row, col) in enumerate(starting_positions):
                self.players.append(
                    Player(
                        ANIMAL_NAMES[i % 4],
                        row,
                        col,
                        (i * 50, i * 10, 255 - i * 50),
                        animal_type=ANIMAL_TYPES[i % 4],
                    )
                )
        else:
            for i in range(players):
                self.players.append(
                    Player(
                        ANIMAL_NAMES[i % 4],
                        0,
                        0,
                        (i * 50, i * 10, 255 - i * 50),
                        animal_type=ANIMAL_TYPES[i % 4],
                    )
                )
        self.met = False
        self.winner_message = ""

    def reset(self):
        for player in self.players:
            player.reset()
        self.met = False
        self.winner_message = ""