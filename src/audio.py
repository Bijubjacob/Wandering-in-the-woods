import os
import sys
import pygame


def resource_path(relative_path):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    return os.path.join(project_root, relative_path)


class AudioManager:
    def __init__(self):
        self.audio_enabled = False
        self.background_channel = None
        self.background_sound = None
        self.meet_path = None
        self.meet_sound = None

        self.partial_meet_start = 0.0
        self.partial_meet_duration_ms = 1200
        self.all_met_start = 5.12

        self._initialize_audio()

    def _initialize_audio(self):
        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init()
            self.audio_enabled = True
        except pygame.error:
            self.audio_enabled = False
            return

        background_candidates = [
            resource_path(os.path.join("assets", "audio", "background.ogg")),
        ]
        meet_candidates = [
            resource_path(os.path.join("assets", "audio", "meet.flac")),
        ]

        self.background_sound = self._load_sound(background_candidates)
        self.meet_path = self._first_existing(meet_candidates)
        if self.meet_path:
            self.meet_sound = self._load_sound([self.meet_path])

    def _first_existing(self, paths):
        for path in paths:
            if os.path.exists(path):
                return path
        return None

    def _load_sound(self, paths):
        for path in paths:
            if not os.path.exists(path):
                continue
            try:
                return pygame.mixer.Sound(path)
            except pygame.error:
                continue
        return None

    def start_background(self):
        if not self.audio_enabled or not self.background_sound:
            return
        if self.background_channel and self.background_channel.get_busy():
            return

        self.background_channel = pygame.mixer.Channel(0)
        self.background_channel.set_volume(0.35)
        self.background_channel.play(self.background_sound, loops=-1)

    def stop_background(self):
        if self.background_channel:
            self.background_channel.fadeout(700)

    def _play_meet_segment(self, start_seconds):
        if not self.audio_enabled or not self.meet_path:
            return
        try:
            pygame.mixer.music.load(self.meet_path)
            pygame.mixer.music.set_volume(0.9)
            pygame.mixer.music.play(loops=0, start=start_seconds, fade_ms=80)
        except pygame.error:
            if self.meet_sound:
                self.meet_sound.set_volume(0.9)
                self.meet_sound.play()

    def play_partial_meet(self):
        if not self.audio_enabled:
            return
        if self.meet_sound:
            self.meet_sound.set_volume(0.9)
            self.meet_sound.play(maxtime=self.partial_meet_duration_ms)
            return
        self._play_meet_segment(self.partial_meet_start)

    def play_all_met(self):
        self._play_meet_segment(self.all_met_start)