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
# The movement logic is handled by the engine.
# This file only handles the interface.
# -----------------------------------------------------------

import tkinter as tk
import os
import pygame
import sys
from engine import create_game, step
from src.game import Game

def is_frozen():
    return getattr(sys, 'frozen', False)

def launch_g35(root):
    
    # create new window
    window = tk.Toplevel(root)
    window.title("Grades 3-5 Mode")
    window.geometry("900x600")

    # creating frame for pygame window
    pygame_frame = tk.Frame(window, width=600, height=600)
    pygame_frame.pack(side=tk.LEFT, padx=10, pady=10)
    
    # Stores user input for starting positions
    starting_positions = []
    
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
    # Defines a canvas to show player placement
    # -----------------------------------------------------------
    
    placement_canvas = tk.Canvas(window, width=400, height=400, bg="white")
    placement_canvas.pack(pady=10)
    
    # -----------------------------------------------------------
    # Draws the grid for player placement and returns cell size and offsets
    # -----------------------------------------------------------
    
    def draw_placement_grid():
        placement_canvas.delete("all")

        w = int(width_entry.get())
        h = int(height_entry.get())

        cw = placement_canvas.winfo_width()
        ch = placement_canvas.winfo_height()
        cell = min(cw / w, ch / h)

        x0 = (cw - cell * w) / 2
        y0 = (ch - cell * h) / 2

        for col in range(w + 1):
            x = x0 + col * cell
            placement_canvas.create_line(x, y0, x, y0 + cell * h)

        for row in range(h + 1):
            y = y0 + row * cell
            placement_canvas.create_line(x0, y, x0 + cell * w, y)

        return cell, x0, y0
    
    # -----------------------------------------------------------
    # Draws player positions on the placement canvas
    # -----------------------------------------------------------
    
    def on_grid_click(event):
        nonlocal starting_positions

        players = int(player_entry.get())
        if len(starting_positions) >= players:
            return

        w = int(width_entry.get())
        h = int(height_entry.get())

        cell, x0, y0 = draw_placement_grid()

        gx = int((event.x - x0) // cell)
        gy = int((event.y - y0) // cell)

        if 0 <= gx < w and 0 <= gy < h:
            if (gx, gy) not in starting_positions:
                starting_positions.append((gx, gy))
                draw_players(cell, x0, y0)

            if len(starting_positions) == players:
                info_label.config(text="All players placed. Ready to run!")
    placement_canvas.bind("<Button-1>", on_grid_click)
    
    # -----------------------------------------------------------
    # Bind click event to the placement canvas
    # -----------------------------------------------------------
    
    def draw_players(cell, x0, y0):
        draw_placement_grid()

        colors = ["red", "blue", "green", "orange"]

        for i, (x, y) in enumerate(starting_positions):
            cx = x0 + (x + 0.5) * cell
            cy = y0 + (y + 0.5) * cell
            r = cell * 0.3

            placement_canvas.create_oval(
                cx - r, cy - r, cx + r, cy + r,
                fill=colors[i % len(colors)]
            )
            placement_canvas.create_text(cx, cy, text=str(i + 1), fill="white")

    # -----------------------------------------------------------
    # Function to start player placement
    # -----------------------------------------------------------

    def start_placement():
        starting_positions.clear()
        info_label.config(text="Click on the grid to place players.")
        draw_placement_grid()

    place_button = tk.Button(
        window,
        text="Choose Starting Positions",
        command=start_placement
    )
    place_button.pack(pady=5)

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

        # validate starting positions
        if len(starting_positions) != players:
            info_label.config(text="Please place all players first.")
            return

        # create the game
        # state = create_game(width, height, starting_positions)
         
        pygame.init()
        
        if not is_frozen():
                window.update_idletasks()
                window.update()
                os.environ["SDL_WINDOWID"] = str(pygame_frame.winfo_id())
                os.environ["SDL_VIDEODRIVER"] = "windib"
                
        screen = pygame.display.set_mode((800, 800))

        game = Game(screen, rows=height, cols=width, players=players, starting_positions=starting_positions)
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