import time

import pygame


class Timer:
    def __init__(self, lj_game):
        """Inicjalizacja atrybutów timera"""
        self.screen = lj_game.screen
        self.screen_rect = self.screen.get_rect()

        self.settings = lj_game.settings
        self.stats = lj_game.stats

        self.timer_color = (255, 0, 0)

        self.last_time = 0

        self.timeout = False
        self.power_up_sound = pygame.mixer.Sound('sounds/power_up.wav')

        self.prep_timer()

    def prep_timer(self):
        """Przekształcenie timera na wygenerowany obraz"""

        self.screen_width = self.screen.get_width()
        self.screen_height = self.screen.get_height()

        self.timer_width = 10 * self.stats.time_left
        self.timer_height = 20 * self.screen_height / 450

        self.rect = pygame.Rect(self.screen_width / 2 - self.timer_width / 2,
                                self.screen_height - 20 * self.screen_height / 450 - 20,
                                self.timer_width, self.timer_height)

    def draw(self):
        self.screen.fill(self.timer_color, self.rect)

    def update(self):
        now = time.time()
        if not self.last_time:
            self.last_time = now
        delta_time = now - self.last_time
        self.stats.time_left -= delta_time
        self.last_time = now

    def increase_time(self):
        if self.stats.score % 10000 == 0:
            self.stats.time_left += 5
            self.power_up_sound.play()

        if self.stats.score < 10000:
            self.stats.time_left += 20 / self.stats.score + 0.18
        if 10000 < self.stats.score < 20000:
            self.stats.time_left += 20 / self.stats.score + 0.15
        if 20000 < self.stats.score < 40000:
            self.stats.time_left += 20 / self.stats.score + 0.14
        if 40000 < self.stats.score < 80000:
            self.stats.time_left += 20 / self.stats.score + 0.135
        if self.stats.score > 80000:
            self.stats.time_left += 20 / self.stats.score + 0.129
