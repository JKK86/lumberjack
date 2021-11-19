import sys
import pygame

from landscape import Cloud, LandscapeBaseClass, Bee, Tree, Lumberjack, BranchProvider
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

        self.branches = pygame.sprite.Group()

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
        self.lumberjack_ready.set_position(
            (self.trunk.x - 0.5 * self.trunk.rect.width - self.lumberjack_ready.rect.width,
             self.screen_height * self.settings.lumberjack_scale - self.lumberjack_ready.rect.height))
        self.lumberjack_hit.set_position(
            (self.trunk.x - 0.5 * self.trunk.rect.width - self.lumberjack_ready.rect.width + 16,
             self.screen_height * self.settings.lumberjack_scale - self.lumberjack_hit.rect.height))

        self.hit = False
        self.lumberjack_on_left = True

        self._create_branches()

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
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        if event.key == pygame.K_ESCAPE:
            sys.exit()
        elif event.key == pygame.K_f:
            self._change_fullscreen()
        elif event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
            self.hit = True
            if event.key == pygame.K_LEFT and not self.lumberjack_on_left:
                self.lumberjack_ready.flip(True, False)
                self.lumberjack_hit.flip(True, False)
                self.lumberjack_on_left = True
                self.lumberjack_ready.x -= 3.44 * self.trunk.rect.width
                self.lumberjack_ready.rect.x = self.lumberjack_ready.x
                self.lumberjack_hit.x -= 2 * self.trunk.rect.width
                self.lumberjack_hit.rect.x = self.lumberjack_hit.x
            if event.key == pygame.K_RIGHT and self.lumberjack_on_left:
                self.lumberjack_ready.flip(True, False)
                self.lumberjack_hit.flip(True, False)
                self.lumberjack_on_left = False
                self.lumberjack_ready.x += 3.44 * self.trunk.rect.width
                self.lumberjack_ready.rect.x = self.lumberjack_ready.x
                self.lumberjack_hit.x += 2 * self.trunk.rect.width
                self.lumberjack_hit.rect.x = self.lumberjack_hit.x

    def _check_keyup_events(self, event):
        if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
            self.hit = False

    def _change_fullscreen(self):
        if self.settings.fullscreen:
            self.settings.fullscreen = False
            surface_size = self.screen.get_size()
            self.screen = pygame.display.set_mode(
                (self.settings.screen_width, self.settings.screen_height),
                pygame.RESIZABLE)
            self._scale_to(self.scalable, surface_size, (self.settings.screen_width, self.settings.screen_height))
            for branch in self.branches.sprites():
                branch.scale(surface_size, (self.settings.screen_width, self.settings.screen_height))
        else:
            self.settings.fullscreen = True
            surface_size = self.screen.get_size()
            self.screen = pygame.display.set_mode(
                (self.settings.fullscreen_width, self.settings.fullscreen_height), pygame.FULLSCREEN)
            self._scale_to(self.scalable, surface_size,
                           (self.settings.fullscreen_width, self.settings.fullscreen_height))
            for branch in self.branches.sprites():
                branch.scale(surface_size, (self.settings.fullscreen_width, self.settings.fullscreen_height))
        self.bee.set_screen(self.screen)
        # self.trunk.set_position((self.screen.get_width() / 2 - self.trunk.rect.width / 2, 0))

    def _scale_to(self, objects: list, old_size, new_size, change_pos=True):
        for obj in objects:
            obj.scale(old_size, new_size, change_pos)

    def _create_branches(self):
        for _ in range(self.settings.branch_count):
            self._create_branch()
            self._create_branch(left=False)
        for branch in self.branches.sprites():
            branch.scale((self.settings.bg_width, self.settings.bg_height),
                         (self.settings.screen_width, self.settings.screen_height),
                         change_pos=False)

    def _create_branch(self, left=True):
        if left:
            branch = BranchProvider(self, 'konar_lewy.png',
                                    position=(self.settings.branch_scale_left * self.screen_width, 100))
        else:
            branch = BranchProvider(self, 'konar_prawy.png',
                                    position=(self.settings.branch_scale_right * self.screen_width, 100))
        self.branches.add(branch)

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

        self.slice_wood.blit_me()

        if self.hit:
            self.trunk_base.blit_me()
            self.trunk.blit_me()
            self.lumberjack_hit.blit_me()
        else:
            self.tree.blit_me()
            self.lumberjack_ready.blit_me()

        self.branches.draw(self.screen)

        pygame.display.flip()
        self.clock.tick(self.settings.FPS)


if __name__ == '__main__':
    lj = LumberjackGame()
    lj.run_game()
