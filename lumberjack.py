import sys
import pygame

from landscape import Cloud, LandscapeBaseClass, Bee, Tree, Lumberjack
from settings import Settings


class LumberjackGame:

    def __init__(self):
        pygame.init()

        self.clock = pygame.time.Clock()

        self.settings = Settings()
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height), pygame.RESIZABLE)
        self.screen_width = self.screen.get_width()
        self.screen_height = self.screen.get_height()

        self.background = LandscapeBaseClass(self, 'background.png')
        self.clouds = [Cloud(self, f'chmurka_0{i}.png', i) for i in range(1, self.settings.number_of_clouds + 1)]
        self.bee = Bee(self, 'bee_01.png', position=(self.screen.get_width() - 100, self.screen.get_height() / 2))
        self.trunk = Tree(self, 'pien_solo.png')
        self.trunk_base = Tree(self, 'pien_podstawa.png')
        self.tree = Tree(self, 'pien_caly.png')
        self.slice_wood = Tree(self, 'plaster_drewna.png')
        self.lumberjack_ready = Lumberjack(self, 'drwal_01.png')
        self.lumberjack_hit = Lumberjack(self, 'drwal_02.png')

        self.scalable = [self.background, self.bee, self.trunk, self.trunk_base, self.tree,
                         self.slice_wood, self.lumberjack_ready, self.lumberjack_hit] + self.clouds

        self._scale_to(self.scalable,
                       (self.settings.bg_width, self.settings.bg_height),
                       (self.settings.screen_width, self.settings.screen_height),
                       change_pos=False)
        self.trunk.set_position((self.screen_width / 2 - self.trunk.rect.width / 2, 0))
        self.trunk_base.set_position((
            self.screen_width / 2 - self.trunk_base.rect.width / 2 + 1.8,
            self.trunk.rect.height))
        self.tree.set_position((self.screen_width / 2 - self.tree.rect.width / 2,
                                self.screen_height - self.tree.rect.height + 11))
        self.slice_wood.set_position((self.screen_width / 2 - self.slice_wood.rect.width / 2,
                                      self.screen_height * self.settings.slice_wood_scale))
        self.lumberjack_ready.set_position((self.trunk.x - 0.5 * self.trunk.rect.width - self.lumberjack_ready.rect.width,
                                            self.screen_height * self.settings.lumberjack_scale - self.lumberjack_ready.rect.height))
        self.lumberjack_hit.set_position((self.trunk.x - 0.5 * self.trunk.rect.width - self.lumberjack_ready.rect.width + 16,
                                            self.screen_height * self.settings.lumberjack_scale - self.lumberjack_hit.rect.height))

        pygame.display.set_caption("Lumberjack")

    def run_game(self):

        while True:
            self._check_events()
            self._update_clouds()
            self._update_bee()
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
        self.bee.set_screen(self.screen)
        # self.trunk.set_position((self.screen.get_width() / 2 - self.trunk.rect.width / 2, 0))

    def _scale_to(self, objects: list, old_size, new_size, change_pos=True):
        for obj in objects:
            obj.scale(old_size, new_size, change_pos)

    def _update_clouds(self):
        screen_width = self.screen.get_width()
        for i, cloud in enumerate(self.clouds):
            cloud.x += self.settings.cloud_speed[i] * (screen_width / self.settings.bg_width)
            cloud.rect.x = cloud.x
            if cloud.rect.x > screen_width:
                cloud.x = -cloud.rect.width
                cloud.rect.x = cloud.x

    def _update_bee(self):
        if self.bee.check_edges():
            self.settings.bee_direction *= -1
            self.bee.flip(True, False)
            self.bee.change_height()
        self.bee.update()

    def _update_screen(self):
        self.screen.fill(self.settings.bg_color)
        self.background.blit_me()
        for cloud in self.clouds:
            cloud.blit_me()
        self.bee.blit_me()
        self.trunk_base.blit_me()
        self.slice_wood.blit_me()
        self.trunk.blit_me()
        # self.tree.blit_me()
        self.lumberjack_ready.blit_me()
        self.lumberjack_hit.blit_me()

        pygame.display.flip()
        self.clock.tick(self.settings.FPS)


if __name__ == '__main__':
    lj = LumberjackGame()
    lj.run_game()
