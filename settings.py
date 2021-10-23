import pygame


class Settings:
    def __init__(self):
        self.screen_width = 1200
        self.screen_height = 800
        self.fullscreen = False
        self.fullscreen_width = 1920
        self.fullscreen_height = 1080

        self.bg_color = (150, 150, 0)
        self.FPS = 60
        self.background = pygame.image.load('images/background.png')
        self.bg_rect = self.background.get_rect()
