import pygame


class Grid:
    def __init__(self, rows=5, cols=5, cell_size=100, margin_top=80, margin_left=0):
        self.rows = rows
        self.cols = cols
        self.cell_size = cell_size
        self.margin_top = margin_top
        self.margin_left = margin_left

        self.width = self.cols * self.cell_size
        self.height = self.rows * self.cell_size

    def draw(self, screen):
        for row in range(self.rows):
            for col in range(self.cols):
                rect = pygame.Rect(
                    self.margin_left + col * self.cell_size,
                    self.margin_top + row * self.cell_size,
                    self.cell_size,
                    self.cell_size,
                )
                pygame.draw.rect(screen, (139, 69, 19), rect, 1)

    def get_cell_center(self, row, col):
        x = self.margin_left + col * self.cell_size + self.cell_size // 2
        y = self.margin_top + row * self.cell_size + self.cell_size // 2
        return x, y

    def is_valid_position(self, row, col):
        return 0 <= row < self.rows and 0 <= col < self.cols