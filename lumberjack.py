import sys
import pygame

from landscape import Cloud, Landscape
from settings import Settings


class Lumberjack:

    def __init__(self):
        pygame.init()

        self.clock = pygame.time.Clock()

        self.settings = Settings()

        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height), pygame.RESIZABLE)

        self.background = Landscape(self, 'background.png')
        self.clouds = [Cloud(self, f'chmurka_0{i}.png', i) for i in range(1, self.settings.number_of_clouds + 1)]
        self.scalable = [self.background] + self.clouds

        self._scale_to(self.scalable,
                       (self.settings.bg_width, self.settings.bg_height),
                       (self.settings.screen_width, self.settings.screen_height))

        pygame.display.set_caption("Lumberjack")

    def run_game(self):

        while True:
            self._check_events()
            self._update_clouds()
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
            surface_size = self.screen.get_size()
            self.screen = pygame.display.set_mode(
                (self.settings.screen_width, self.settings.screen_height),
                pygame.RESIZABLE)
            self._scale_to(self.scalable, surface_size, (self.settings.screen_width, self.settings.screen_height))
        else:
            self.settings.fullscreen = True
            surface_size = self.screen.get_size()
            self.screen = pygame.display.set_mode(
                (self.settings.fullscreen_width, self.settings.fullscreen_height), pygame.FULLSCREEN)
            self._scale_to(self.scalable, surface_size,
                           (self.settings.fullscreen_width, self.settings.fullscreen_height))

    def _scale_to(self, objects: list, old_size, new_size):
        for obj in objects:
            obj.scale(old_size, new_size)

    def _update_clouds(self):
        screen_width = self.screen.get_width()
        for i, cloud in enumerate(self.clouds):
            cloud.x += self.settings.cloud_speed[i] * (screen_width / self.settings.bg_width)
            cloud.rect.x = cloud.x
            if cloud.rect.x > screen_width:
                cloud.x = -cloud.rect.width
                cloud.rect.x = cloud.x

    def _update_screen(self):
        self.screen.fill(self.settings.bg_color)
        self.background.blit_me()
        for cloud in self.clouds:
            cloud.blit_me()
        pygame.display.flip()
        self.clock.tick(self.settings.FPS)


if __name__ == '__main__':
    lj = Lumberjack()
    lj.run_game()
