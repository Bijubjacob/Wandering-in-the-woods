import pygame
import os
import sys


def resource_path(relative_path: str) -> str:
    """
    Get absolute path to resource.
    """
    if hasattr(sys, "_MEIPASS"):
        base_path = sys._MEIPASS
    else:
        # audio.py is in src/, so go up one level to project root
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

    return os.path.join(base_path, relative_path)


class AudioManager:
    def __init__(self):
        self.meet_sound = None
        self.background_path = None

        assets_dir = resource_path("src/assets")

        meet_path = os.path.join(assets_dir, "meet.flac")
        self.background_path = os.path.join(assets_dir, "background.ogg")

        print("AudioManager: assets_dir =", assets_dir)
        print("AudioManager: meet =", meet_path)
        print("AudioManager: background =", self.background_path)

        # ---------------------------------
        # Load meet sound
        # ---------------------------------

        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init()

            self.meet_sound = pygame.mixer.Sound(meet_path)
            self.meet_sound.set_volume(1.0)
            print("AudioManager: meet sound loaded")

        except Exception as e:
            print("AudioManager WARNING: meet sound failed to load")
            print("Reason:", e)
            self.meet_sound = None

    # ---------------------------------
    # Background music
    # ---------------------------------

    def start_background(self):
        if not self.background_path:
            return

        try:
            pygame.mixer.music.load(self.background_path)
            pygame.mixer.music.set_volume(0.4)
            pygame.mixer.music.play(loops=-1)
            print("AudioManager: background music started")

        except Exception as e:
            print("AudioManager WARNING: background music failed")
            print("Reason:", e)

    def stop_background(self):
        try:
            pygame.mixer.music.fadeout(1000)
        except Exception:
            pass

    # ---------------------------------
    # Meet sound
    # ---------------------------------

    def play_meet_sound(self):
        if self.meet_sound:
            try:
                self.meet_sound.play()
            except Exception:
                pass