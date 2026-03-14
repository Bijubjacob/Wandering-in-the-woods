# -----------------------------------------------------------
# GRADES 3–5 MODE
#
# This version is slightly more complex than the K-2 mode.
# Students can:
# - choose grid size
# - choose number of players (2–4)
# - choose starting positions of players
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
from src.game import Game


def launch_g35(root):

    # create new window
    window = tk.Toplevel(root)
    window.title("Grades 3-5 Mode")
    window.geometry("1100x700")

    # Main split layout: left for simulation, right for controls.
    main_frame = tk.Frame(window)
    main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    pygame_frame = tk.Frame(main_frame, width=700, height=680, bg="black", relief=tk.SUNKEN, bd=2)
    pygame_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 12))
    pygame_frame.pack_propagate(False)

    controls_frame = tk.LabelFrame(main_frame, text="Simulation Controls", padx=10, pady=10)
    controls_frame.pack(side=tk.RIGHT, fill=tk.Y)

    window.update_idletasks()
    os.environ["SDL_WINDOWID"] = str(pygame_frame.winfo_id())
    if os.name == "nt":
        os.environ["SDL_VIDEODRIVER"] = "windib"

    # -----------------------------------------------------------
    # USER INPUT SETTINGS
    # -----------------------------------------------------------

    tk.Label(controls_frame, text="Grid Width").grid(row=0, column=0, sticky="w", pady=(0, 2))
    width_entry = tk.Entry(controls_frame)
    width_entry.insert(0, "8")
    width_entry.grid(row=1, column=0, sticky="ew", pady=(0, 8))

    tk.Label(controls_frame, text="Grid Height").grid(row=2, column=0, sticky="w", pady=(0, 2))
    height_entry = tk.Entry(controls_frame)
    height_entry.insert(0, "8")
    height_entry.grid(row=3, column=0, sticky="ew", pady=(0, 8))

    tk.Label(controls_frame, text="Number of Players (2-4)").grid(row=4, column=0, sticky="w", pady=(0, 2))
    player_entry = tk.Entry(controls_frame)
    player_entry.insert(0, "2")
    player_entry.grid(row=5, column=0, sticky="ew", pady=(0, 8))

    tk.Label(controls_frame, text="Starting Positions (click cells)").grid(row=6, column=0, sticky="w", pady=(4, 2))
    placement_canvas = tk.Canvas(controls_frame, width=280, height=280, bg="white", highlightthickness=1)
    placement_canvas.grid(row=7, column=0, sticky="ew", pady=(0, 6))

    stats_label = tk.Label(controls_frame, text="Runs: 0", justify=tk.LEFT, anchor="w")
    stats_label.grid(row=9, column=0, sticky="ew", pady=(8, 4))

    info_label = tk.Label(controls_frame, text="", justify=tk.LEFT, anchor="w", wraplength=260)
    info_label.grid(row=10, column=0, sticky="ew", pady=(0, 8))

    controls_frame.grid_columnconfigure(0, weight=1)

    # -----------------------------------------------------------
    # STATISTICS VARIABLES
    # -----------------------------------------------------------

    runs = []  # list storing number of steps for each run

    def get_simulation_surface_size():
        window.update_idletasks()
        width = max(400, pygame_frame.winfo_width() - 4)
        height = max(400, pygame_frame.winfo_height() - 4)
        return width, height

    start_positions = []

    def get_player_count():
        try:
            return max(2, min(int(player_entry.get()), 4))
        except ValueError:
            return 2

    def get_grid_dimensions():
        try:
            width = max(1, int(width_entry.get()))
            height = max(1, int(height_entry.get()))
            return width, height
        except ValueError:
            return 8, 8

    def draw_placement_grid():
        placement_canvas.delete("all")
        width, height = get_grid_dimensions()

        canvas_width = placement_canvas.winfo_width()
        canvas_height = placement_canvas.winfo_height()
        cell = min(canvas_width / width, canvas_height / height)
        x0 = (canvas_width - cell * width) / 2
        y0 = (canvas_height - cell * height) / 2

        for col in range(width + 1):
            x = x0 + col * cell
            placement_canvas.create_line(x, y0, x, y0 + cell * height)

        for row in range(height + 1):
            y = y0 + row * cell
            placement_canvas.create_line(x0, y, x0 + cell * width, y)

        return cell, x0, y0

    def draw_players(cell, x0, y0):
        draw_placement_grid()
        animals = ["rabbit", "fox", "owl", "raccoon"]

        def draw_animal_icon(cx, cy, size, animal, label):
            if animal == "rabbit":
                # Ears
                placement_canvas.create_oval(cx - size * 0.35, cy - size * 0.9, cx - size * 0.1, cy - size * 0.3, fill="#f3f4f6", outline="#9ca3af")
                placement_canvas.create_oval(cx + size * 0.1, cy - size * 0.9, cx + size * 0.35, cy - size * 0.3, fill="#f3f4f6", outline="#9ca3af")
                # Head
                placement_canvas.create_oval(cx - size * 0.5, cy - size * 0.45, cx + size * 0.5, cy + size * 0.45, fill="#e5e7eb", outline="#9ca3af")
            elif animal == "fox":
                # Head
                placement_canvas.create_polygon(
                    cx, cy - size * 0.55,
                    cx - size * 0.6, cy + size * 0.45,
                    cx + size * 0.6, cy + size * 0.45,
                    fill="#f97316",
                    outline="#9a3412",
                )
                # Muzzle
                placement_canvas.create_polygon(
                    cx, cy + size * 0.05,
                    cx - size * 0.22, cy + size * 0.45,
                    cx + size * 0.22, cy + size * 0.45,
                    fill="#fff7ed",
                    outline="#9a3412",
                )
            elif animal == "owl":
                # Body
                placement_canvas.create_oval(cx - size * 0.55, cy - size * 0.55, cx + size * 0.55, cy + size * 0.55, fill="#92400e", outline="#451a03")
                # Eyes
                placement_canvas.create_oval(cx - size * 0.35, cy - size * 0.25, cx - size * 0.05, cy + size * 0.05, fill="white", outline="#1f2937")
                placement_canvas.create_oval(cx + size * 0.05, cy - size * 0.25, cx + size * 0.35, cy + size * 0.05, fill="white", outline="#1f2937")
                placement_canvas.create_oval(cx - size * 0.24, cy - size * 0.15, cx - size * 0.13, cy - size * 0.04, fill="#111827", outline="#111827")
                placement_canvas.create_oval(cx + size * 0.13, cy - size * 0.15, cx + size * 0.24, cy - size * 0.04, fill="#111827", outline="#111827")
                # Beak
                placement_canvas.create_polygon(cx, cy - size * 0.02, cx - size * 0.11, cy + size * 0.16, cx + size * 0.11, cy + size * 0.16, fill="#f59e0b", outline="#92400e")
            else:
                # Raccoon face
                placement_canvas.create_oval(cx - size * 0.55, cy - size * 0.5, cx + size * 0.55, cy + size * 0.5, fill="#9ca3af", outline="#4b5563")
                # Mask
                placement_canvas.create_oval(cx - size * 0.48, cy - size * 0.16, cx + size * 0.48, cy + size * 0.16, fill="#374151", outline="#1f2937")
                # Eyes
                placement_canvas.create_oval(cx - size * 0.25, cy - size * 0.12, cx - size * 0.1, cy + size * 0.04, fill="white", outline="#111827")
                placement_canvas.create_oval(cx + size * 0.1, cy - size * 0.12, cx + size * 0.25, cy + size * 0.04, fill="white", outline="#111827")
                placement_canvas.create_oval(cx - size * 0.2, cy - size * 0.07, cx - size * 0.14, cy - size * 0.01, fill="#111827", outline="#111827")
                placement_canvas.create_oval(cx + size * 0.14, cy - size * 0.07, cx + size * 0.2, cy - size * 0.01, fill="#111827", outline="#111827")

            placement_canvas.create_text(cx, cy + size * 0.62, text=label, fill="#111827", font=("Arial", max(8, int(size * 0.32)), "bold"))

        for idx, (x, y) in enumerate(start_positions):
            cx = x0 + (x + 0.5) * cell
            cy = y0 + (y + 0.5) * cell
            size = max(8, cell * 0.35)
            draw_animal_icon(cx, cy, size, animals[idx % len(animals)], str(idx + 1))

    def on_grid_click(event):
        players = get_player_count()
        if len(start_positions) >= players:
            return

        width, height = get_grid_dimensions()
        cell, x0, y0 = draw_placement_grid()
        grid_x = int((event.x - x0) // cell)
        grid_y = int((event.y - y0) // cell)

        if 0 <= grid_x < width and 0 <= grid_y < height and (grid_x, grid_y) not in start_positions:
            start_positions.append((grid_x, grid_y))
            draw_players(cell, x0, y0)

            if len(start_positions) == players:
                info_label.config(text="All players placed. Ready to run.")
            else:
                info_label.config(text=f"Placed {len(start_positions)}/{players}. Keep placing players.")

    placement_canvas.bind("<Button-1>", on_grid_click)

    def start_placement():
        start_positions.clear()
        draw_placement_grid()
        info_label.config(text="Click the mini-grid to place each player.")

    def update_start_fields(_event=None):
        active_players = get_player_count()
        if len(start_positions) > active_players:
            del start_positions[active_players:]
        cell, x0, y0 = draw_placement_grid()
        draw_players(cell, x0, y0)

    # -----------------------------------------------------------
    # FUNCTION TO RUN ONE SIMULATION
    # -----------------------------------------------------------

    def run_simulation():

        # get user input values
        try:
            width = int(width_entry.get())
            height = int(height_entry.get())
            players = int(player_entry.get())
        except ValueError:
            info_label.config(text="Grid size and players must be whole numbers.")
            return

        if width <= 0 or height <= 0:
            info_label.config(text="Grid width and height must be greater than 0.")
            return

        # limit players between 2 and 4
        players = max(2, min(players, 4))
        player_entry.delete(0, tk.END)
        player_entry.insert(0, str(players))
        update_start_fields()

        if len(start_positions) != players:
            info_label.config(text=f"Place all players first ({len(start_positions)}/{players}).")
            return

        info_label.config(text="")

        pygame.init()
        sim_width, sim_height = get_simulation_surface_size()
        screen = pygame.display.set_mode((sim_width, sim_height))

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
            stats_label.config(text="Runs: 0")
            return

        shortest = min(runs)
        longest = max(runs)
        average = sum(runs) / len(runs)

        stats_label.config(
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
        controls_frame,
        text="Run Simulation",
        command=run_simulation
    )
    run_button.grid(row=11, column=0, sticky="ew", pady=(4, 6))

    reset_button = tk.Button(
        controls_frame,
        text="Reset Statistics",
        command=lambda: (runs.clear(), update_stats(), info_label.config(text=""))
    )
    reset_button.grid(row=12, column=0, sticky="ew")

    place_button = tk.Button(
        controls_frame,
        text="Choose Starting Positions",
        command=start_placement,
    )
    place_button.grid(row=8, column=0, sticky="ew", pady=(0, 2))

    player_entry.bind("<KeyRelease>", update_start_fields)
    player_entry.bind("<FocusOut>", update_start_fields)
    width_entry.bind("<KeyRelease>", update_start_fields)
    width_entry.bind("<FocusOut>", update_start_fields)
    height_entry.bind("<KeyRelease>", update_start_fields)
    height_entry.bind("<FocusOut>", update_start_fields)
    update_start_fields()
    start_placement()


# For testing g35 mode independently
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # hide main window
    launch_g35(root)
    root.mainloop()