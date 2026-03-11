import pygame
from src.grid import Grid
from src.simulation import Simulation
from src.stats import Stats
from src.ui import UI
from src.audio import AudioManager


class Game:
    def __init__(self, screen, rows=5, cols=5):
        # self.screen_width = 500
        # self.screen_height = 650
        self.screen = screen
        pygame.display.set_caption("Wandering in the Woods")

        self.clock = pygame.time.Clock()
        self.ui = UI()
        self.audio = AudioManager()

        self.grid = Grid(rows, cols, cell_size=100, margin_top=100)
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

                # elif event.type == pygame.KEYDOWN:
                #     if event.key == pygame.K_r:
                #         self.reset_game()

            if not self.simulation.met:
                self.simulation.players[0].move_random(self.grid)
                self.check_meeting()
                self.simulation.players[1].move_random(self.grid)
                self.check_meeting()
            else:
                running = False

            #self.update()
            self.draw()
            # Change FPS here
            self.clock.tick(3)