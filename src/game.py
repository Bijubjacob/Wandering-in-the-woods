import pygame
from grid import Grid
from simulation import Simulation
from stats import Stats
from ui import UI
from audio import AudioManager


class Game:
    def __init__(self):
        self.screen_width = 500
        self.screen_height = 650
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Wandering in the Woods")

        self.clock = pygame.time.Clock()
        self.ui = UI()
        self.audio = AudioManager()

        self.grid = Grid(rows=5, cols=5, cell_size=100, margin_top=100)
        self.simulation = Simulation(self.grid)
        self.stats = Stats()

        self.meet_time = None
        self.background_color = (34, 139, 34)

    def reset_game(self):
        self.simulation.reset()
        self.meet_time = None

    def check_meeting(self):
        if (
            self.simulation.players[0].row == self.simulation.players[1].row
            and self.simulation.players[0].col == self.simulation.players[1].col
        ):
            self.simulation.met = True
            self.simulation.winner_message = "They found each other!"
            self.audio.play_meet_sound()
            self.stats.record_run()
            self.meet_time = pygame.time.get_ticks()

    def update(self):
        current_time = pygame.time.get_ticks()

        if self.simulation.met and self.meet_time:
            if current_time - self.meet_time >= 2000:
                self.reset_game()

    def draw(self):
        self.screen.fill(self.background_color)

        self.ui.draw_text(self.screen, "Wandering in the Woods", 110, 20)
        self.ui.draw_text(
            self.screen,
            f"Player 1 moves: {self.simulation.players[0].move_count}",
            20,
            60,
            small=True,
        )
        self.ui.draw_text(
            self.screen,
            f"Player 2 moves: {self.simulation.players[1].move_count}",
            250,
            60,
            small=True,
        )

        self.grid.draw(self.screen)

        for player in self.simulation.players:
            player.draw(self.screen, self.grid)

        self.ui.draw_text(
            self.screen,
            "P1: W A S D    P2: Arrow Keys    R: Reset",
            20,
            610,
            (255, 255, 255),
            small=True,
        )

        if self.simulation.met:
            self.ui.draw_text(
                self.screen,
                self.simulation.winner_message,
                120,
                580,
                (255, 255, 0),
            )

        pygame.display.flip()

    def run(self):
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.reset_game()

                    elif not self.simulation.met:
                        # Player 1 - WASD
                        if event.key == pygame.K_w:
                            self.simulation.players[0].move(-1, 0, self.grid)
                            self.check_meeting()
                        elif event.key == pygame.K_s:
                            self.simulation.players[0].move(1, 0, self.grid)
                            self.check_meeting()
                        elif event.key == pygame.K_a:
                            self.simulation.players[0].move(0, -1, self.grid)
                            self.check_meeting()
                        elif event.key == pygame.K_d:
                            self.simulation.players[0].move(0, 1, self.grid)
                            self.check_meeting()

                        # Player 2 - Arrow Keys
                        elif event.key == pygame.K_UP:
                            self.simulation.players[1].move(-1, 0, self.grid)
                            self.check_meeting()
                        elif event.key == pygame.K_DOWN:
                            self.simulation.players[1].move(1, 0, self.grid)
                            self.check_meeting()
                        elif event.key == pygame.K_LEFT:
                            self.simulation.players[1].move(0, -1, self.grid)
                            self.check_meeting()
                        elif event.key == pygame.K_RIGHT:
                            self.simulation.players[1].move(0, 1, self.grid)
                            self.check_meeting()

            self.update()
            self.draw()
            self.clock.tick(60)