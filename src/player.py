import random
import pygame


class Player:
    def __init__(self, name, row, col, color):
        self.name = name
        self.start_row = row
        self.start_col = col
        self.row = row
        self.col = col
        self.color = color
        self.move_count = 0

    def move(self, d_row, d_col, grid):
        new_row = self.row + d_row
        new_col = self.col + d_col

        if grid.is_valid_position(new_row, new_col):
            self.row = new_row
            self.col = new_col
            self.move_count += 1

    def move_random(self, grid):
        directions = [
            (-1, 0),  # up
            (1, 0),   # down
            (0, -1),  # left
            (0, 1),   # right
        ]

        random.shuffle(directions)

        for d_row, d_col in directions:
            new_row = self.row + d_row
            new_col = self.col + d_col

            if grid.is_valid_position(new_row, new_col):
                self.row = new_row
                self.col = new_col
                self.move_count += 1
                return

    def reset(self):
        self.row = self.start_row
        self.col = self.start_col
        self.move_count = 0

    def draw(self, screen, grid):
        x, y = grid.get_cell_center(self.row, self.col)
        pygame.draw.circle(screen, self.color, (x, y), grid.cell_size // 4)