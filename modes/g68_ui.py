
# -----------------------------------------------------------
# GRADES 6-8 MODE
#
# This version is for older students.
# Students can:
# - choose grid width and height
# - choose number of players
# - choose how many trials to run
# - run many simulations
# - see statistics from many runs
# - view a simple graph of the results
#
# This file handles the interface.
# The game logic is handled by the engine.
# -----------------------------------------------------------

import tkinter as tk
import os
import pygame
import matplotlib.pyplot as plt
import sys
from tkinter import messagebox
from src.game import Game

def is_frozen():
    return getattr(sys, 'frozen', False)

def launch_g68(root):
    """
    Opens the Grades 6-8 window
    """
    
    # create a new window
    window = tk.Toplevel(root)
    window.title("Grades 6–8 Mode")
    window.geometry("1100x700")

    # create frame for pygame window
    pygame_frame = tk.Frame(window, width=700, height=700)
    pygame_frame.pack(side=tk.LEFT, padx=10, pady=10)

    # Create controls on the right side
    controls = tk.Frame(window)
    controls.pack(side=tk.RIGHT, fill=tk.Y, padx=10)

    # -----------------------------------------------------------
    # USER INPUT SETTINGS
    # -----------------------------------------------------------
    
    tk.Label(controls, text="Grid Width").pack()
    width_entry = tk.Entry(controls)
    width_entry.insert(0, "10")
    width_entry.pack()

    tk.Label(controls, text="Grid Height").pack()
    height_entry = tk.Entry(controls)
    height_entry.insert(0, "10")
    height_entry.pack()

    tk.Label(controls, text="Players (2–4)").pack()
    player_entry = tk.Entry(controls)
    player_entry.insert(0, "4")
    player_entry.pack()

    tk.Label(controls, text="Number of Trials").pack()
    trials_entry = tk.Entry(controls)
    trials_entry.insert(0, "5")
    trials_entry.pack()

    info_label = tk.Label(controls, text="", justify="left")
    info_label.pack(pady=10)

    # -----------------------------------------------------------
    # PLAYER PLACEMENT CANVAS
    # -----------------------------------------------------------

    placement_canvas = tk.Canvas(controls, width=300, height=300, bg="white")
    placement_canvas.pack(pady=10)

    starting_positions = []

    def draw_placement_grid():
        placement_canvas.delete("all")

        w = int(width_entry.get())
        h = int(height_entry.get())

        cw = placement_canvas.winfo_width()
        ch = placement_canvas.winfo_height()
        cell = min(cw / w, ch / h)

        x0 = (cw - cell * w) / 2
        y0 = (ch - cell * h) / 2

        for i in range(w + 1):
            x = x0 + i * cell
            placement_canvas.create_line(x, y0, x, y0 + cell * h)

        for j in range(h + 1):
            y = y0 + j * cell
            placement_canvas.create_line(x0, y, x0 + cell * w, y)

        return cell, x0, y0

    def draw_players(cell, x0, y0):
        draw_placement_grid()
        colors = ["red", "blue", "green", "orange"]

        for i, (x, y) in enumerate(starting_positions):
            cx = x0 + (x + 0.5) * cell
            cy = y0 + (y + 0.5) * cell
            r = cell * 0.3
            placement_canvas.create_oval(
                cx - r, cy - r, cx + r, cy + r,
                fill=colors[i % 4]
            )
            placement_canvas.create_text(cx, cy, text=str(i + 1), fill="white")

    def on_grid_click(event):
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
                info_label.config(text="All players placed.")

    placement_canvas.bind("<Button-1>", on_grid_click)

    def start_placement():
        starting_positions.clear()
        info_label.config(text="Click grid to place players.")
        draw_placement_grid()

    tk.Button(
        controls,
        text="Choose Starting Positions",
        command=start_placement
    ).pack(pady=5)

    # -----------------------------------------------------------
    # FUNCTION TO RUN THE EXPERIMENT
    # -----------------------------------------------------------

    results = []

    def run_experiment():
        nonlocal results
        results = []

        width = int(width_entry.get())
        height = int(height_entry.get())
        players = max(2, min(int(player_entry.get()), 4))
        trials = int(trials_entry.get())

        if len(starting_positions) != players:
            messagebox.showerror("Error", "Place all players first.")
            return

        results.clear()

        for trial in range(trials):
            pygame.init()

            if not is_frozen():
                window.update_idletasks()
                window.update()
                os.environ["SDL_WINDOWID"] = str(pygame_frame.winfo_id())
                os.environ["SDL_VIDEODRIVER"] = "windib"

            screen = pygame.display.set_mode((800, 800))

            game = Game(
                screen,
                rows=height,
                cols=width,
                players=players,
                starting_positions=starting_positions
            )

            meet_time = game.run()
            results.append(meet_time)

            pygame.quit()
        update_results()

    # -----------------------------------------------------------
    # FUNCTION TO UPDATE RESULTS LABEL
    # -----------------------------------------------------------

    def update_results():
        shortest = min(results)
        longest = max(results)
        average = sum(results) / len(results)

        info_label.config(
            text=(
                f"Trials: {len(results)}\n"
                f"Shortest: {shortest}\n"
                f"Longest: {longest}\n"
                f"Average: {average:.2f}"
            )
        )

    # -----------------------------------------------------------
    # FUNCTION TO SHOW GRAPH
    # -----------------------------------------------------------

    def show_graph():
        if not results:
            return

        plt.figure()
        plt.plot(range(1, len(results) + 1), results, marker="o")
        plt.title("Wandering in the Woods – G6–8")
        plt.xlabel("Trial")
        plt.ylabel("Steps Until Meeting")
        plt.show(block=False)

    # -----------------------------------------------------------
    # BUTTONS
    # -----------------------------------------------------------

    tk.Button(
        controls,
        text="Run Experiment",
        command=run_experiment
    ).pack(pady=5)

    tk.Button(
        controls,
        text="Show Graph",
        command=show_graph
    ).pack(pady=5)
