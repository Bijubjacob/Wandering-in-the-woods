import tkinter as tk
import os
import pygame
from src.game import Game



def launch_k2(root):

	window = tk.Toplevel(root)
	window.title("K-2 Mode")
	window.geometry("1000x700")

	main_frame = tk.Frame(window)
	main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

	pygame_frame = tk.Frame(main_frame, width=700, height=680, bg="black", relief=tk.SUNKEN, bd=2)
	pygame_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 12))
	pygame_frame.pack_propagate(False)

	controls_frame = tk.LabelFrame(main_frame, text="K-2 Controls", padx=10, pady=10)
	controls_frame.pack(side=tk.RIGHT, fill=tk.Y)

	window.update_idletasks()
	os.environ["SDL_WINDOWID"] = str(pygame_frame.winfo_id())
	if os.name == "nt":
		os.environ["SDL_VIDEODRIVER"] = "windib"

	tk.Label(controls_frame, text="Grid Size (NxN)").grid(row=0, column=0, sticky="w", pady=(0, 2))
	size_entry = tk.Entry(controls_frame)
	size_entry.insert(0, "8")
	size_entry.grid(row=1, column=0, sticky="ew", pady=(0, 8))

	rule_label = tk.Label(
		controls_frame,
		justify=tk.LEFT,
		anchor="w",
		text=(
			"K-2 Rules:\n"
			"- Rabbit & Fox wander the woods\n"
			"- Start at opposite corners\n"
			"- No run statistics"
		),
	)
	rule_label.grid(row=2, column=0, sticky="ew", pady=(0, 10))

	info_label = tk.Label(controls_frame, text="", justify=tk.LEFT, anchor="w", wraplength=260)
	info_label.grid(row=3, column=0, sticky="ew", pady=(0, 8))

	controls_frame.grid_columnconfigure(0, weight=1)

	def get_simulation_surface_size():
		window.update_idletasks()
		width = max(400, pygame_frame.winfo_width() - 4)
		height = max(400, pygame_frame.winfo_height() - 4)
		return width, height

	def run_simulation():
		try:
			grid_size = int(size_entry.get())
		except ValueError:
			info_label.config(text="Grid size must be a whole number.")
			return

		if grid_size < 2:
			info_label.config(text="Grid size must be at least 2 for opposite-corner starts.")
			return

		info_label.config(text="")

		start_positions = [(0, 0), (grid_size - 1, grid_size - 1)]

		pygame.init()
		sim_width, sim_height = get_simulation_surface_size()
		screen = pygame.display.set_mode((sim_width, sim_height))

		game = Game(
			screen,
			rows=grid_size,
			cols=grid_size,
			players=2,
			starting_positions=start_positions,
		)
		game.run()
		pygame.quit()

	run_button = tk.Button(
		controls_frame,
		text="Run Simulation",
		command=run_simulation,
	)
	run_button.grid(row=4, column=0, sticky="ew")


if __name__ == "__main__":
	root = tk.Tk()
	root.withdraw()
	launch_k2(root)
	root.mainloop()

 