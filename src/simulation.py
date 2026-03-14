from src.player import Player

ANIMAL_TYPES = ["rabbit", "fox", "owl", "raccoon"]
ANIMAL_NAMES = ["Rabbit", "Fox", "Owl", "Raccoon"]


class Simulation:
    def __init__(self, grid, players, starting_positions=None):
        self.grid = grid
        self.players = []
        if starting_positions:
            normalized_positions = self._normalize_starting_positions(starting_positions, players)
            for i, (row, col) in enumerate(normalized_positions):
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

    def _normalize_starting_positions(self, starting_positions, players):
        normalized = []

        for position in starting_positions:
            if not isinstance(position, (tuple, list)) or len(position) != 2:
                continue

            first, second = position
            try:
                first = int(first)
                second = int(second)
            except (TypeError, ValueError):
                continue

            if self.grid.is_valid_position(first, second):
                candidate = (first, second)
            elif self.grid.is_valid_position(second, first):
                candidate = (second, first)
            else:
                continue

            if candidate not in normalized:
                normalized.append(candidate)
            if len(normalized) == players:
                return normalized

        if len(normalized) < players:
            for row in range(self.grid.rows):
                for col in range(self.grid.cols):
                    candidate = (row, col)
                    if candidate not in normalized:
                        normalized.append(candidate)
                    if len(normalized) == players:
                        return normalized

        return normalized

    def reset(self):
        for player in self.players:
            player.reset()
        self.met = False
        self.winner_message = ""