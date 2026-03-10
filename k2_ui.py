import tkinter as tk
from engine.engine import create_game, step


def launch_k2(root):

    window = tk.Toplevel(root)
    window.title("K-2 Mode")

    size = 6

    state = create_game(
        size,
        size,
        [(0, 0), (size - 1, size - 1)]
    )

    label = tk.Label(window, text="Press Start")
    label.pack(pady=10)

    running = False

    def run():

        nonlocal running

        if not running:
            return

        step(state)

        label.config(
            text=f"Step: {state.time_steps} Positions: {[g.position for g in state.groups]}"
        )

        window.after(500, run)

    def start():

        nonlocal running

        running = True

        run()

    button = tk.Button(window, text="Start", command=start)
    button.pack()