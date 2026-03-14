import random
import pygame


ANIMAL_SPEEDS = {
    "rabbit": 1.4,
    "fox": 1.15,
    "raccoon": 0.9,
    "owl": 0.7,
}


class Player:
    def __init__(self, name, row, col, color, animal_type="rabbit"):
        self.name = name
        self.start_row = row
        self.start_col = col
        self.row = row
        self.col = col
        self.color = color
        self.move_count = 0
        self.direction_index = 0
        self.spiral_direction_index = 0
        self.spiral_visited = {(self.row, self.col)}
        self.animal_type = animal_type
        self.group_animal_types = [animal_type]
        self.move_progress = 0.0

    def get_speed(self):
        return min(ANIMAL_SPEEDS.get(animal_type, 1.0) for animal_type in self.group_animal_types)

    def get_moves_for_tick(self):
        self.move_progress += self.get_speed()
        steps = int(self.move_progress)
        self.move_progress -= steps
        return steps

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

    def move_clockwise(self, grid):
        directions = [
            (0, 1),   # right
            (1, 0),   # down
            (0, -1),  # left
            (-1, 0),  # up
        ]

        for offset in range(len(directions)):
            direction_idx = (self.direction_index + offset) % len(directions)
            d_row, d_col = directions[direction_idx]
            new_row = self.row + d_row
            new_col = self.col + d_col

            if grid.is_valid_position(new_row, new_col):
                self.row = new_row
                self.col = new_col
                self.move_count += 1
                self.direction_index = direction_idx
                return

    def move_zigzag(self, grid):
        if self.row % 2 == 0:
            preferred_directions = [
                (0, 1),   # right
                (1, 0),   # down to next row at right edge
                (0, -1),  # then back left if needed
                (-1, 0),  # fallback up
            ]
        else:
            preferred_directions = [
                (0, -1),  # left
                (1, 0),   # down to next row at left edge
                (0, 1),   # then back right if needed
                (-1, 0),  # fallback up
            ]

        for d_row, d_col in preferred_directions:
            new_row = self.row + d_row
            new_col = self.col + d_col

            if grid.is_valid_position(new_row, new_col):
                self.row = new_row
                self.col = new_col
                self.move_count += 1
                return

    def move_spiral(self, grid):
        directions = [
            (0, 1),   # right
            (1, 0),   # down
            (0, -1),  # left
            (-1, 0),  # up
        ]

        # Prefer unexplored cells while turning clockwise when blocked.
        for offset in range(len(directions)):
            direction_idx = (self.spiral_direction_index + offset) % len(directions)
            d_row, d_col = directions[direction_idx]
            new_row = self.row + d_row
            new_col = self.col + d_col

            if (
                grid.is_valid_position(new_row, new_col)
                and (new_row, new_col) not in self.spiral_visited
            ):
                self.row = new_row
                self.col = new_col
                self.move_count += 1
                self.spiral_direction_index = direction_idx
                self.spiral_visited.add((self.row, self.col))
                return

        # If every neighbor was visited already, keep moving clockwise.
        for offset in range(len(directions)):
            direction_idx = (self.spiral_direction_index + offset) % len(directions)
            d_row, d_col = directions[direction_idx]
            new_row = self.row + d_row
            new_col = self.col + d_col

            if grid.is_valid_position(new_row, new_col):
                self.row = new_row
                self.col = new_col
                self.move_count += 1
                self.spiral_direction_index = direction_idx
                self.spiral_visited.add((self.row, self.col))
                return

    def reset(self):
        self.row = self.start_row
        self.col = self.start_col
        self.move_count = 0
        self.direction_index = 0
        self.spiral_direction_index = 0
        self.spiral_visited = {(self.row, self.col)}
        self.group_animal_types = [self.animal_type]
        self.move_progress = 0.0

    def draw(self, screen, grid):
        x, y = grid.get_cell_center(self.row, self.col)
        size = max(6, grid.cell_size // 4)
        n = len(self.group_animal_types)
        if n == 1:
            self._draw_animal(screen, x, y, size, self.group_animal_types[0])
        else:
            sub_size = max(4, int(size * 0.65))
            for animal_type, (dx, dy) in zip(self.group_animal_types, self._group_offsets(n, sub_size)):
                self._draw_animal(screen, x + dx, y + dy, sub_size, animal_type)

    def _group_offsets(self, n, size):
        half = max(1, size // 2)
        if n == 2:
            return [(-half, 0), (half, 0)]
        elif n == 3:
            return [(-half, -half // 2), (half, -half // 2), (0, half // 2)]
        else:
            return [(-half, -half // 2), (half, -half // 2), (-half, half // 2), (half, half // 2)]

    def _draw_animal(self, screen, x, y, size, animal_type):
        if animal_type == "rabbit":
            self._draw_rabbit(screen, x, y, size)
        elif animal_type == "fox":
            self._draw_fox(screen, x, y, size)
        elif animal_type == "owl":
            self._draw_owl(screen, x, y, size)
        else:
            self._draw_raccoon(screen, x, y, size)

    def _draw_rabbit(self, screen, x, y, size):
        body_color = (220, 220, 220)
        inner_ear = (255, 170, 190)
        eye_color = (0, 0, 0)

        pygame.draw.ellipse(screen, body_color, (x - size // 2, y - size // 2, size, size))
        pygame.draw.ellipse(screen, body_color, (x - size // 3, y - int(size * 1.2), size // 3, size))
        pygame.draw.ellipse(screen, body_color, (x + size // 12, y - int(size * 1.2), size // 3, size))
        pygame.draw.ellipse(screen, inner_ear, (x - size // 4, y - int(size * 1.1), size // 8, int(size * 0.7)))
        pygame.draw.ellipse(screen, inner_ear, (x + size // 6, y - int(size * 1.1), size // 8, int(size * 0.7)))
        pygame.draw.circle(screen, eye_color, (x - size // 6, y - size // 8), max(1, size // 12))
        pygame.draw.circle(screen, eye_color, (x + size // 6, y - size // 8), max(1, size // 12))

    def _draw_fox(self, screen, x, y, size):
        fur = (235, 120, 40)
        white = (245, 245, 245)
        eye_color = (0, 0, 0)

        head_points = [(x, y - size // 2), (x - size // 2, y + size // 3), (x + size // 2, y + size // 3)]
        left_ear = [(x - size // 3, y - size // 2), (x - size // 2, y - size), (x - size // 7, y - size // 2)]
        right_ear = [(x + size // 3, y - size // 2), (x + size // 2, y - size), (x + size // 7, y - size // 2)]
        muzzle = [(x, y), (x - size // 5, y + size // 3), (x + size // 5, y + size // 3)]

        pygame.draw.polygon(screen, fur, left_ear)
        pygame.draw.polygon(screen, fur, right_ear)
        pygame.draw.polygon(screen, fur, head_points)
        pygame.draw.polygon(screen, white, muzzle)
        pygame.draw.circle(screen, eye_color, (x - size // 6, y - size // 8), max(1, size // 12))
        pygame.draw.circle(screen, eye_color, (x + size // 6, y - size // 8), max(1, size // 12))

    def _draw_owl(self, screen, x, y, size):
        brown = (120, 85, 60)
        light = (220, 210, 190)
        eye_ring = (240, 240, 220)
        eye_color = (20, 20, 20)

        pygame.draw.circle(screen, brown, (x, y), size // 2)
        pygame.draw.ellipse(screen, light, (x - size // 4, y, size // 2, size // 3))
        pygame.draw.circle(screen, eye_ring, (x - size // 6, y - size // 8), max(2, size // 6))
        pygame.draw.circle(screen, eye_ring, (x + size // 6, y - size // 8), max(2, size // 6))
        pygame.draw.circle(screen, eye_color, (x - size // 6, y - size // 8), max(1, size // 12))
        pygame.draw.circle(screen, eye_color, (x + size // 6, y - size // 8), max(1, size // 12))
        beak = [(x, y - size // 20), (x - size // 10, y + size // 10), (x + size // 10, y + size // 10)]
        pygame.draw.polygon(screen, (240, 190, 40), beak)

    def _draw_raccoon(self, screen, x, y, size):
        gray = (160, 160, 165)
        dark = (60, 60, 65)
        light = (220, 220, 225)
        eye_color = (15, 15, 15)

        pygame.draw.ellipse(screen, gray, (x - size // 2, y - size // 2, size, size))
        pygame.draw.circle(screen, dark, (x - size // 3, y - size // 2), max(2, size // 6))
        pygame.draw.circle(screen, dark, (x + size // 3, y - size // 2), max(2, size // 6))
        pygame.draw.rect(screen, dark, (x - size // 2, y - size // 8, size, size // 3))
        pygame.draw.ellipse(screen, light, (x - size // 4, y, size // 2, size // 4))
        pygame.draw.circle(screen, eye_color, (x - size // 6, y - size // 12), max(1, size // 12))
        pygame.draw.circle(screen, eye_color, (x + size // 6, y - size // 12), max(1, size // 12))
