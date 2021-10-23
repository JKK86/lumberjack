import sys
import pygame

from settings import Settings


class Lumberjack:

    def __init__(self):
        pygame.init()

        self.clock = pygame.time.Clock()

        self.settings = Settings()
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height), pygame.RESIZABLE)

        pygame.display.set_caption("Lumberjack")

    def run_game(self):

        while True:
            self._check_events()
            self._update_screen()

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)

    def _check_keydown_events(self, event):
        if event.key == pygame.K_ESCAPE:
            sys.exit()
        elif event.key == pygame.K_f:
            self._change_fullscreen()

    def _change_fullscreen(self):
        if self.settings.fullscreen:
            self.settings.fullscreen = False
            self.screen = pygame.display.set_mode(
                (self.settings.screen_width, self.settings.screen_height),
                pygame.RESIZABLE)
        else:
            self.settings.fullscreen = True
            self.screen = pygame.display.set_mode(
                (self.settings.fullscreen_width, self.settings.fullscreen_height), pygame.FULLSCREEN)

    def _update_screen(self):
        self.screen.fill(self.settings.bg_color)

        self.screen.blit(self.settings.background, self.settings.bg_rect)
        pygame.display.flip()
        self.clock.tick(self.settings.FPS)


if __name__ == '__main__':
    lj = Lumberjack()
    lj.run_game()
