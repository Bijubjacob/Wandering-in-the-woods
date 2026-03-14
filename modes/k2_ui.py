# -----------------------------------------------------------
# K–2 MODE
#
# Simplest version:
# - fixed grid
# - 2 players
# - visual movement
# - background audio
# - meet sound
# - clear success message
# -----------------------------------------------------------

import tkinter as tk
import os
import pygame
import sys
from src.game import Game

def is_frozen():
    return getattr(sys, 'frozen', False)

def launch_k2(root):

    window = tk.Toplevel(root)
    window.title("K–2 Mode")
    window.geometry("900x650")

    # -----------------------------------------------------------
    # Create the frame for the pygame window
    # -----------------------------------------------------------

    pygame_frame = tk.Frame(window, width=600, height=600)
    pygame_frame.pack(padx=10, pady=10)

    # -----------------------------------------------------------
    # UI LABEL
    # -----------------------------------------------------------

    info_label = tk.Label(
        window,
        text="Press Start to watch the friends find each other!",
        font=("Arial", 14)
    )
    info_label.pack(pady=10)

    # -----------------------------------------------------------
    # RUN SIMULATION
    # -----------------------------------------------------------

    def start_simulation():

        info_label.config(text="They are walking in the woods...")

        pygame.init()
        
        if not is_frozen():   
                window.update_idletasks()
                window.update()
                os.environ["SDL_WINDOWID"] = str(pygame_frame.winfo_id())
                os.environ["SDL_VIDEODRIVER"] = "windib"
                
        screen = pygame.display.set_mode((600, 600))

        # Fixed, simple setup for K–2
        size = 6
        starting_positions = [
            (0, 0),
            (size - 1, size - 1)
        ]

        game = Game(
            screen,
            rows=size,
            cols=size,
            players=2,
            starting_positions=starting_positions
        )

        game.run()
        pygame.quit()

        info_label.config(text="🎉 They found each other! 🎉")

    # -----------------------------------------------------------
    # START BUTTON
    # -----------------------------------------------------------

    tk.Button(
        window,
        text="Start",
        font=("Arial", 16),
        command=start_simulation
    ).pack(pady=10)


# For testing independently
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    launch_k2(root)
    root.mainloop()
