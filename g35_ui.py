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

    tk.Label(controls_frame, text="Starting Positions").grid(row=6, column=0, sticky="w", pady=(4, 2))

    start_position_entries = []
    start_position_labels = []
    animal_names = ["Rabbit", "Fox", "Owl", "Raccoon"]
    default_positions = ["0,0", "1,0", "2,0", "3,0"]
    for i in range(4):
        label = tk.Label(controls_frame, text=f"{animal_names[i]} Start (x,y)")
        label.grid(row=7 + i * 2, column=0, sticky="w", pady=(0, 2))
        entry = tk.Entry(controls_frame)
        entry.insert(0, default_positions[i])
        entry.grid(row=8 + i * 2, column=0, sticky="ew", pady=(0, 6))
        start_position_labels.append(label)
        start_position_entries.append(entry)

    stats_label = tk.Label(controls_frame, text="Runs: 0", justify=tk.LEFT, anchor="w")
    stats_label.grid(row=16, column=0, sticky="ew", pady=(8, 4))

    info_label = tk.Label(controls_frame, text="", justify=tk.LEFT, anchor="w", wraplength=260)
    info_label.grid(row=17, column=0, sticky="ew", pady=(0, 8))

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

    def get_player_count():
        try:
            return max(2, min(int(player_entry.get()), 4))
        except ValueError:
            return 2

    def update_start_fields(_event=None):
        active_players = get_player_count()
        for idx, (label, entry) in enumerate(zip(start_position_labels, start_position_entries), start=1):
            if idx <= active_players:
                label.config(fg="black")
                entry.config(state=tk.NORMAL)
            else:
                label.config(fg="gray45")
                entry.config(state=tk.DISABLED)

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

        # parse starting positions from user input (x,y for each player)
        start_positions = []
        for i in range(players):
            raw_value = start_position_entries[i].get().strip()
            try:
                x_text, y_text = raw_value.split(",")
                x = int(x_text.strip())
                y = int(y_text.strip())
            except ValueError:
                info_label.config(text=f"Invalid start position for Player {i + 1}. Use x,y.")
                return

            if x < 0 or x >= width or y < 0 or y >= height:
                info_label.config(
                    text=(
                        f"Player {i + 1} start must be inside the grid "
                        f"(x: 0-{width - 1}, y: 0-{height - 1})."
                    )
                )
                return

            start_positions.append((x, y))

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
    run_button.grid(row=18, column=0, sticky="ew", pady=(4, 6))

    reset_button = tk.Button(
        controls_frame,
        text="Reset Statistics",
        command=lambda: (runs.clear(), update_stats(), info_label.config(text=""))
    )
    reset_button.grid(row=19, column=0, sticky="ew")

    player_entry.bind("<KeyRelease>", update_start_fields)
    player_entry.bind("<FocusOut>", update_start_fields)
    update_start_fields()


# For testing g35 mode independently
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # hide main window
    launch_g35(root)
    root.mainloop()