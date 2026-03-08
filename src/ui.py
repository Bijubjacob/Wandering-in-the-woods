import pygame


class UI:

    def __init__(self):
        self.font = pygame.font.SysFont("arial", 28)
        self.small_font = pygame.font.SysFont("arial", 20)

    def draw_text(self, screen, text, x, y, color=(255, 255, 255), small=False):
        if small:
            text_surface = self.small_font.render(text, True, color)
        else:
            text_surface = self.font.render(text, True, color)

        screen.blit(text_surface, (x, y))