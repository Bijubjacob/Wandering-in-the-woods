import pygame
from src.grid import Grid
from src.simulation import Simulation
from src.ui import UI
from src.audio import AudioManager


class Game:
    def __init__(
        self,
        screen,
        rows=5,
        cols=5,
        players=2,
        starting_positions=None,
        movement_algorithm="random",
    ):
        # self.screen_width = 500
        # self.screen_height = 650
        self.screen = screen
        pygame.mixer.init()
        pygame.display.set_caption("Wandering in the Woods")

        self.clock = pygame.time.Clock()
        self.ui = UI()
        self.audio = AudioManager()

        self.screen_width, self.screen_height = self.screen.get_size()
        self.grid_margin_top = 100
        self.grid_margin_bottom = 80

        max_grid_width = max(1, self.screen_width)
        max_grid_height = max(1, self.screen_height - self.grid_margin_top - self.grid_margin_bottom)
        cell_size = max(4, min(max_grid_width // cols, max_grid_height // rows))
        grid_width = cols * cell_size
        margin_left = max(0, (self.screen_width - grid_width) // 2)

        self.grid = Grid(
            rows,
            cols,
            cell_size=cell_size,
            margin_top=self.grid_margin_top,
            margin_left=margin_left,
        )
        self.simulation = Simulation(self.grid, players, starting_positions)

        self.meet_time = None
        self.final_meet_time = None
        self.final_clap_hold_ms = 2500
        self.background_color = (34, 139, 34)
        self.movement_algorithm = movement_algorithm

    def move_player(self, player):
        steps = player.get_moves_for_tick()
        for _ in range(steps):
            self._move_player_one_step(player)
            self.check_meeting()
            if len(self.simulation.players) == 1:
                return

    def _move_player_one_step(self, player):
        if self.movement_algorithm == "clockwise":
            player.move_clockwise(self.grid)
        elif self.movement_algorithm == "zigzag":
            player.move_zigzag(self.grid)
        elif self.movement_algorithm == "spiral":
            player.move_spiral(self.grid)
        else:
            player.move_random(self.grid)

    def reset_game(self):
        self.simulation.reset()
        self.meet_time = None
        self.final_meet_time = None

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
                        merged_group = (
                            self.simulation.players[i].group_animal_types
                            + self.simulation.players[j].group_animal_types
                        )
                        new_player.name = f"{self.simulation.players[i].name} & {self.simulation.players[j].name}"
                        new_player.color = (255, 255, 255)
                        new_player.group_animal_types = merged_group

                        # Remove the players that met
                        del self.simulation.players[j]
                        del self.simulation.players[i]

                        # Add the new player to the simulation
                        self.simulation.players.append(new_player)

                        # Play different cues for intermediate vs final meeting.
                        if len(self.simulation.players) == 1:
                            self.audio.play_all_met()
                        else:
                            self.audio.play_partial_meet()

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

        self.ui.draw_text(self.screen, "Wandering in the Woods", 20, 20)
        if len(self.simulation.players) >= 1:
            self.ui.draw_text(
                self.screen,
                f"{self.simulation.players[0].name} moves: {self.simulation.players[0].move_count}",
                20,
                60,
                small=True,
            )
        if len(self.simulation.players) >= 2:
            self.ui.draw_text(
                self.screen,
                f"{self.simulation.players[1].name} moves: {self.simulation.players[1].move_count}",
                max(20, self.screen_width // 2),
                60,
                small=True,
            )
        elif len(self.simulation.players) == 1:
            self.ui.draw_text(
                self.screen,
                f"Grouped moves: {self.simulation.players[0].move_count}",
                max(20, self.screen_width // 2),
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
                20,
                self.screen_height - 40,
                (255, 255, 0),
            )

        pygame.display.flip()

    def run(self):
        running = True
        run_start_time = pygame.time.get_ticks()
        run_duration_seconds = 0.0
        self.audio.start_background()

        try:
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
                        self.move_player(player)
                        if len(self.simulation.players) == 1:
                            self.meet_time = pygame.time.get_ticks()
                            run_duration_seconds = max(0.0, (self.meet_time - run_start_time) / 1000.0)
                            self.final_meet_time = self.meet_time
                            break

                if self.final_meet_time is not None:
                    elapsed = pygame.time.get_ticks() - self.final_meet_time
                    if elapsed >= self.final_clap_hold_ms:
                        running = False

                #self.update()
                self.draw()

                # Change FPS here
                self.clock.tick(3)
        finally:
            self.audio.stop_background()

        return run_duration_seconds