import pygame
from src.grid import Grid
from src.simulation import Simulation
from src.stats import Stats
from src.ui import UI
from src.audio import AudioManager


class Game:
    def __init__(self, screen, rows=5, cols=5, players=2, starting_positions=None):
        # self.screen_width = 500
        # self.screen_height = 650
        self.screen = screen
        pygame.display.set_caption("Wandering in the Woods")

        self.clock = pygame.time.Clock()
        self.ui = UI()
        self.audio = AudioManager()

        self.grid = Grid(rows, cols, cell_size=100, margin_top=100)
        self.simulation = Simulation(self.grid, players, starting_positions)
        self.stats = Stats()

        self.meet_time = None
        self.background_color = (34, 139, 34)

    def reset_game(self):
        self.simulation.reset()
        self.meet_time = None

    def check_meeting(self):
        # While players share the same cell, create a new player that has the same position as the players that met, and remove the players that met. 
        # This represents grouping the players together when they meet, and allows the simulation to continue until all players have met.
        is_players_still_meeting = True
        while is_players_still_meeting:
            is_players_met = False
            for i in range(len(self.simulation.players)):
                for j in range(i + 1, len(self.simulation.players)):
                    if (
                        self.simulation.players[i].row == self.simulation.players[j].row
                        and self.simulation.players[i].col == self.simulation.players[j].col
                    ):
                        # Create a new player that has the same position as the players that met
                        new_player = self.simulation.players[i]
                        new_player.name = f"{self.simulation.players[i].name} & {self.simulation.players[j].name}"
                        new_player.color = (255, 255, 255)

                        # Remove the players that met
                        del self.simulation.players[j]
                        del self.simulation.players[i]

                        # Add the new player to the simulation
                        self.simulation.players.append(new_player)

                        # Play meet sound
                        self.audio.play_meet_sound()

                        is_players_met = True
                        break
                if is_players_met:
                    break
            if not is_players_met:
                is_players_still_meeting = False

        if len(self.simulation.players) == 1:
            self.simulation.met = True
            self.simulation.winner_message = f"All players met: {self.simulation.players[0].name}"
            
        #self.simulation.met = True
        #self.simulation.winner_message = "They found each other!"
        #self.audio.play_meet_sound()
        #self.stats.record_run()
        #self.meet_time = pygame.time.get_ticks()

    def update(self):
        current_time = pygame.time.get_ticks()

        if self.simulation.met and self.meet_time:
            if current_time - self.meet_time >= 2000:
                self.reset_game()

    def draw(self):
        self.screen.fill(self.background_color)

        self.ui.draw_text(self.screen, "Wandering in the Woods", 110, 20)
        if len(self.simulation.players) >= 1:
            self.ui.draw_text(
                self.screen,
                f"Player 1 moves: {self.simulation.players[0].move_count}",
                20,
                60,
                small=True,
            )
        if len(self.simulation.players) >= 2:
            self.ui.draw_text(
                self.screen,
                f"Player 2 moves: {self.simulation.players[1].move_count}",
                250,
                60,
                small=True,
            )
        elif len(self.simulation.players) == 1:
            self.ui.draw_text(
                self.screen,
                f"Grouped moves: {self.simulation.players[0].move_count}",
                250,
                60,
                small=True,
            )

        self.grid.draw(self.screen)

        for player in self.simulation.players:
            player.draw(self.screen, self.grid)

        # self.ui.draw_text(
        #     self.screen,
        #     "P1: W A S D    P2: Arrow Keys    R: Reset",
        #     20,
        #     610,
        #     (255, 255, 255),
        #     small=True,
        # )

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

            
            if len(self.simulation.players) > 1:
                for player in list(self.simulation.players):
                    if player not in self.simulation.players:
                        continue
                    player.move_random(self.grid)
                    self.check_meeting()
                    if len(self.simulation.players) == 1:
                        self.meet_time = pygame.time.get_ticks()
                        running = False
                        break

            #self.update()
            self.draw()

            # Change FPS here
            self.clock.tick(3)

        return self.meet_time