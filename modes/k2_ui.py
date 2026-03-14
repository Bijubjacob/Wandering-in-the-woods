import tkinter as tk
import os
import pygame
from src.game import Game
from src.narrator import narrate_async



def launch_k2(root):
	max_side = 15

	window = tk.Toplevel(root)
	window.title("K-2 Mode")
	window.geometry("1000x920")
	try:
		window.state("zoomed")
	except tk.TclError:
		window.geometry(f"{window.winfo_screenwidth()}x{window.winfo_screenheight()}+0+0")

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

	instruction_text = (
		"Instructions:\n"
		"- A Rabbit and Fox wander the woods in a square grid you choose.\n"
		"- They start at opposite corners and try to find each other.\n"
		"- Press Run Simulation to watch them move around the grid.\n"
		"- Try different grid sizes and compare how long it takes for them to meet."
	)
	# Narrator voices this text
	narration_text = (
		"Welcome to K through 2 mode. "
		"Choose a grid size. The rabbit and fox start at opposite corners. "
		"Then run the simulation and see how many moves it takes for them to meet."
	)

	tk.Label(controls_frame, text="Grid Size (NxN, max 15)").grid(row=0, column=0, sticky="w", pady=(0, 2))
	size_entry = tk.Entry(controls_frame)
	size_entry.insert(0, "8")
	size_entry.grid(row=1, column=0, sticky="ew", pady=(0, 8))

	rule_label = tk.Label(
		controls_frame,
		justify=tk.LEFT,
		anchor="w",
		text=instruction_text,
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

	def clamp_size_entry(_event=None):
		value = size_entry.get().strip()
		if not value:
			return
		try:
			grid_size = int(value)
		except ValueError:
			return
		if grid_size > max_side:
			size_entry.delete(0, tk.END)
			size_entry.insert(0, str(max_side))

	def run_simulation():
		try:
			grid_size = int(size_entry.get())
		except ValueError:
			info_label.config(text="Grid size must be a whole number.")
			return

		if grid_size < 2:
			info_label.config(text="Grid size must be at least 2 for opposite-corner starts.")
			return

		if grid_size > max_side:
			grid_size = max_side
			size_entry.delete(0, tk.END)
			size_entry.insert(0, str(max_side))

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

	size_entry.bind("<KeyRelease>", clamp_size_entry)
	size_entry.bind("<FocusOut>", clamp_size_entry)

	narrate_async(narration_text)

	# --- Reflection Questions ---
	quiz_frame = tk.LabelFrame(window, text="Reflection Questions", padx=10, pady=8)
	quiz_frame.pack(fill=tk.X, padx=10, pady=(0, 10))

	quiz_questions = [
		"Q1: Which animal moves the fastest?",
		"Q2: Is there a pattern to the movement of the animals?",
		"Q3: How does the grid size affect the number of steps the animals take to meet?",
	]
	for i, q_text in enumerate(quiz_questions):
		tk.Label(quiz_frame, text=q_text, anchor="w", justify=tk.LEFT).grid(
			row=i, column=0, sticky="w", pady=(6, 0)
		)
	quiz_frame.grid_columnconfigure(0, weight=1)

# For testing mode
if __name__ == "__main__":
	root = tk.Tk()
	root.withdraw()
	launch_k2(root)
	root.mainloop()

 