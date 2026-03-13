# -----------------------------------------------------------
# GRADES 3–5 MODE
#
# This version is slightly more complex than the K-2 mode.
# Students can:
# - choose grid size
# - choose number of players (2–4)
# - run the simulation multiple times
# - view statistics like:
#     shortest run
#     longest run
#     average run
#
# The movement logic is handled by the engine created
# by Person 1. This file only handles the interface.
# -----------------------------------------------------------

import tkinter as tk
import os
import pygame
from engine import create_game, step
from src.game import Game


def launch_g35(root):

    # create new window
    window = tk.Toplevel(root)
    window.title("Grades 3-5 Mode")
    window.geometry("900x600")

    # creating frame for pygame window
    pygame_frame = tk.Frame(window, width=600, height=600)
    pygame_frame.pack(side=tk.LEFT, padx=10, pady=10)

    # Telling pygame to use the tkinter frame for its display
    os.environ["SDL_WINDOWID"] = str(pygame_frame.winfo_id())
    os.environ["SDL_VIDEODRIVER"] = "windib"

    # -----------------------------------------------------------
    # USER INPUT SETTINGS
    # -----------------------------------------------------------

    tk.Label(window, text="Grid Width").pack(side=tk.RIGHT)
    width_entry = tk.Entry(window)
    width_entry.insert(0, "8")
    width_entry.pack(side=tk.RIGHT)

    tk.Label(window, text="Grid Height").pack(side=tk.RIGHT)
    height_entry = tk.Entry(window)
    height_entry.insert(0, "8")
    height_entry.pack(side=tk.RIGHT)

    tk.Label(window, text="Number of Players (2-4)").pack(side=tk.RIGHT)
    player_entry = tk.Entry(window)
    player_entry.insert(0, "2")
    player_entry.pack(side=tk.RIGHT)

    info_label = tk.Label(window, text="")
    info_label.pack(pady=5)

    # -----------------------------------------------------------
    # STATISTICS VARIABLES
    # -----------------------------------------------------------

    runs = []  # list storing number of steps for each run

    # -----------------------------------------------------------
    # FUNCTION TO RUN ONE SIMULATION
    # -----------------------------------------------------------

    def run_simulation():

        # get user input values
        width = int(width_entry.get())
        height = int(height_entry.get())
        players = int(player_entry.get())

        # limit players between 2 and 4
        players = max(2, min(players, 4))

        # generate starting positions automatically
        start_positions = []

        for i in range(players):

            x = i % width
            y = i % height

            start_positions.append((x, y))

        # create the game
        # state = create_game(width, height, start_positions)
         
        pygame.init()
        screen = pygame.display.set_mode((600, 600))

        game = Game(screen, rows=height, cols=width, players=players, starting_positions=start_positions)
        run_time = game.run()
        pygame.quit()


        # run simulation until players meet
        # while not state.finished:
        #     step(state)

        # record the result
        runs.append(run_time)

        update_stats()

    # -----------------------------------------------------------
    # FUNCTION TO UPDATE STATISTICS
    # -----------------------------------------------------------

    def update_stats():

        if not runs:
            return

        shortest = min(runs)
        longest = max(runs)
        average = sum(runs) / len(runs)

        info_label.config(
            text=(
                f"Runs: {len(runs)}\n"
                f"Shortest: {shortest}\n"
                f"Longest: {longest}\n"
                f"Average: {average:.2f}"
            )
        )

    # -----------------------------------------------------------
    # BUTTONS
    # -----------------------------------------------------------

    run_button = tk.Button(
        window,
        text="Run Simulation",
        command=run_simulation
    )
    run_button.pack(pady=10)

    reset_button = tk.Button(
        window,
        text="Reset Statistics",
        command=lambda: runs.clear()
    )
    reset_button.pack()


# For testing g35 mode independently
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # hide main window
    launch_g35(root)
    root.mainloop()