import tkinter as tk
import os
import pygame
from src.game import Game
from src.narrator import narrate_async


def launch_g68(root):
    max_side = 15

    window = tk.Toplevel(root)
    window.title("Grades 6-8 Mode")
    window.geometry("1100x700")

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

    instruction_text = (
        "Instructions:\n"
        "- Choose grid size, player count (2 to 4), and a movement algorithm.\n"
        "- Click Choose Starting Positions, then place all animals on the mini-grid.\n"
        "- Press Run Simulation to run one trial with the selected algorithm.\n"
        "- Repeat runs and compare shortest, longest, and average time in seconds."
    )

    narration_text = (
        "Welcome to Grades 6 through 8 mode. "
        "Set the grid size, number of players, and movement algorithm. "
        "Place all animals on the mini grid, then run a trial. "
        "Repeat and compare the statistics to evaluate algorithm performance."
    )

    tk.Label(controls_frame, text="Grid Width (max 15)").grid(row=0, column=0, sticky="w", pady=(0, 2))
    width_entry = tk.Entry(controls_frame)
    width_entry.insert(0, "8")
    width_entry.grid(row=1, column=0, sticky="ew", pady=(0, 8))

    tk.Label(controls_frame, text="Grid Height (max 15)").grid(row=2, column=0, sticky="w", pady=(0, 2))
    height_entry = tk.Entry(controls_frame)
    height_entry.insert(0, "8")
    height_entry.grid(row=3, column=0, sticky="ew", pady=(0, 8))

    tk.Label(controls_frame, text="Number of Players (2-4)").grid(row=4, column=0, sticky="w", pady=(0, 2))
    player_entry = tk.Entry(controls_frame)
    player_entry.insert(0, "2")
    player_entry.grid(row=5, column=0, sticky="ew", pady=(0, 8))

    tk.Label(controls_frame, text="Movement Algorithm").grid(row=6, column=0, sticky="w", pady=(0, 2))
    movement_var = tk.StringVar(value="Random")
    algorithm_menu = tk.OptionMenu(
        controls_frame,
        movement_var,
        "Random",
        "Clockwise",
        "Zigzag",
        "Spiral",
    )
    algorithm_menu.grid(row=7, column=0, sticky="ew", pady=(0, 8))

    tk.Label(controls_frame, text="Starting Positions (click cells)").grid(row=8, column=0, sticky="w", pady=(4, 2))
    placement_canvas = tk.Canvas(controls_frame, width=280, height=280, bg="white", highlightthickness=1)
    placement_canvas.grid(row=9, column=0, sticky="ew", pady=(0, 6))

    stats_label = tk.Label(controls_frame, text="Runs: 0", justify=tk.LEFT, anchor="w")
    stats_label.grid(row=11, column=0, sticky="ew", pady=(8, 4))

    info_label = tk.Label(controls_frame, text="", justify=tk.LEFT, anchor="w", wraplength=260)
    info_label.grid(row=12, column=0, sticky="ew", pady=(0, 8))

    instructions_label = tk.Label(
        controls_frame,
        text=instruction_text,
        justify=tk.LEFT,
        anchor="w",
        wraplength=260,
    )
    instructions_label.grid(row=13, column=0, sticky="ew", pady=(2, 8))

    controls_frame.grid_columnconfigure(0, weight=1)

    runs = []

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

    start_positions = []

    def get_grid_dimensions():
        try:
            width = min(max_side, max(1, int(width_entry.get())))
            height = min(max_side, max(1, int(height_entry.get())))
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

    def clamp_dimension_entry(entry_widget):
        value = entry_widget.get().strip()
        if not value:
            return
        try:
            dimension = int(value)
        except ValueError:
            return
        if dimension > max_side:
            entry_widget.delete(0, tk.END)
            entry_widget.insert(0, str(max_side))

    def update_start_fields(_event=None):
        clamp_dimension_entry(width_entry)
        clamp_dimension_entry(height_entry)
        active_players = get_player_count()
        if len(start_positions) > active_players:
            del start_positions[active_players:]
        cell, x0, y0 = draw_placement_grid()
        draw_players(cell, x0, y0)

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
                f"Shortest: {shortest:.2f} s\n"
                f"Longest: {longest:.2f} s\n"
                f"Average: {average:.2f} s"
            )
        )

    def run_simulation():
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

        if width > max_side:
            width = max_side
            width_entry.delete(0, tk.END)
            width_entry.insert(0, str(max_side))

        if height > max_side:
            height = max_side
            height_entry.delete(0, tk.END)
            height_entry.insert(0, str(max_side))

        players = max(2, min(players, 4))
        player_entry.delete(0, tk.END)
        player_entry.insert(0, str(players))
        update_start_fields()

        if len(start_positions) != players:
            info_label.config(text=f"Place all players first ({len(start_positions)}/{players}).")
            return

        movement_algorithm = "random"
        if movement_var.get() == "Clockwise":
            movement_algorithm = "clockwise"
        elif movement_var.get() == "Zigzag":
            movement_algorithm = "zigzag"
        elif movement_var.get() == "Spiral":
            movement_algorithm = "spiral"

        info_label.config(text="")

        pygame.init()
        sim_width, sim_height = get_simulation_surface_size()
        screen = pygame.display.set_mode((sim_width, sim_height))

        game = Game(
            screen,
            rows=height,
            cols=width,
            players=players,
            starting_positions=start_positions,
            movement_algorithm=movement_algorithm,
        )
        run_time = game.run()
        pygame.quit()

        runs.append(run_time)
        update_stats()

    run_button = tk.Button(
        controls_frame,
        text="Run Simulation",
        command=run_simulation,
    )
    run_button.grid(row=14, column=0, sticky="ew", pady=(4, 6))

    reset_button = tk.Button(
        controls_frame,
        text="Reset Statistics",
        command=lambda: (runs.clear(), update_stats(), info_label.config(text="")),
    )
    reset_button.grid(row=15, column=0, sticky="ew")

    place_button = tk.Button(
        controls_frame,
        text="Choose Starting Positions",
        command=start_placement,
    )
    place_button.grid(row=10, column=0, sticky="ew", pady=(0, 2))

    player_entry.bind("<KeyRelease>", update_start_fields)
    player_entry.bind("<FocusOut>", update_start_fields)
    width_entry.bind("<KeyRelease>", update_start_fields)
    width_entry.bind("<FocusOut>", update_start_fields)
    height_entry.bind("<KeyRelease>", update_start_fields)
    height_entry.bind("<FocusOut>", update_start_fields)
    update_start_fields()
    start_placement()
    narrate_async(narration_text)


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    launch_g68(root)
    root.mainloop()