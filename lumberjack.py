import random
import sys
import pygame

import pygame.font

from game_stats import GameStats
from highscores import Highscores
from landscape import Cloud, LandscapeBaseClass, Bee, Tree, Lumberjack, BranchProvider
from scoreboard import Scoreboard
from settings import Settings
from timer import Timer


class LumberjackGame:

    def __init__(self):
        pygame.init()

        self.clock = pygame.time.Clock()

        self.settings = Settings()
        self.stats = GameStats(self)

        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height), pygame.RESIZABLE)
        self.screen_width = self.screen.get_width()
        self.screen_height = self.screen.get_height()

        self.hs = Highscores(self)

        self.font = pygame.font.Font('fonts/bungee-regular.ttf', 50)

        self.background = LandscapeBaseClass(self, 'background.png')
        self.clouds = [Cloud(self, f'chmurka_0{i}.png', i) for i in range(1, self.settings.number_of_clouds + 1)]
        self.bee = Bee(self, 'bee_01.png', position=(self.screen_width - 100, self.screen_height / 2))
        self.trunk = Tree(self, 'pien_solo.png')
        self.trunk_base = Tree(self, 'pien_podstawa.png')
        self.tree = Tree(self, 'pien_caly.png')
        self.slice_wood = Tree(self, 'plaster_drewna.png')
        self.lumberjack_ready = Lumberjack(self, 'drwal_01.png')
        self.lumberjack_hit = Lumberjack(self, 'drwal_02.png')
        self.grave = LandscapeBaseClass(self, 'rip.png', position=(self.screen_width / 4, self.screen_height * (2 / 3)))

        self.branches_left = [self._create_branch() for _ in range(self.settings.branch_count)]
        self.branches_right = [self._create_branch(left=False) for _ in range(self.settings.branch_count)]
        self.branches = []

        self.scalable = [self.background, self.bee, self.trunk, self.trunk_base, self.tree,
                         self.slice_wood, self.lumberjack_ready, self.lumberjack_hit, self.grave,
                         self.hs.board, self.hs.tag] + self.clouds

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

        self.hs.board.set_position((self.screen_width / 2 - self.hs.board.rect.width / 2,
                                      self.screen_height / 2 - self.hs.board.rect.height / 2))
        # self.hs.tag.rect.center = self.screen.get_rect().center
        self.hs.tag.set_position((self.screen_width / 2 - self.hs.tag.rect.width / 2,
                                    self.screen_height / 2 - self.hs.tag.rect.height / 2))

        self.hit = False
        self.lumberjack_on_left = True

        self.last_taken_left = 0
        self.last_taken_right = 0
        self.top = 0

        self._create_branches()

        self.collision = False

        self.sb = Scoreboard(self)

        self.timer = Timer(self)

        self.text_editor_mode = False

        self.hit_sound = pygame.mixer.Sound('sounds/hit_tree.wav')
        self.fail_sound = pygame.mixer.Sound('sounds/groan.wav')
        pygame.mixer.music.load('music/lumberjack_theme.mp3')
        pygame.mixer.music.play(-1)

        pygame.display.set_caption("Lumberjack")

    def run_game(self):

        while True:
            self._check_events()

            if self.stats.game_active:
                self._update_clouds()
                self._update_bee()
                self._update_timer()

            self._update_screen()

    def _start_game(self):
        self.stats.reset_stats()
        self.stats.game_active = True
        self.timer.reset_timer()
        self.collision = False
        self.hit = False
        self.hs.name = ''
        self.sb.prep_score()
        self.timer.prep_timer()
        pygame.mixer.music.load('music/nature.mp3')
        pygame.mixer.music.play(-1)

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
        if self.text_editor_mode:
            self.hs.append_player_name(pygame.key.name(event.key))
        elif event.key == pygame.K_RETURN and not self.stats.game_active and not self.text_editor_mode:
            self._start_game()
        elif event.key == pygame.K_f:
            self._change_fullscreen()
        if self.stats.game_active:
            if event.key == pygame.K_LEFT:
                self.collision = self._check_lumberjack_branch_collision('left')
                if self.collision:
                    self.fail_sound.play()
                self._update_slice_wood((self.screen_width - self.slice_wood.rect.width / 2, self.screen_height / 2))
            if event.key == pygame.K_RIGHT:
                self.collision = self._check_lumberjack_branch_collision('right')
                if self.collision:
                    self.fail_sound.play()
                self._update_slice_wood((0 - self.slice_wood.rect.width / 2, self.screen_height / 2))
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                self.hit = True
                self._hit_tree()
                self.hit_sound.play()
                self.stats.score += 10
                self.sb.prep_score()
                self.sb.check_high_score()
                self.timer.increase_time()
                self.timer.prep_timer()

                if event.key == pygame.K_LEFT and not self.lumberjack_on_left:
                    self._flip_lumberjack(flip_direction=-1)
                    self.lumberjack_on_left = True
                if event.key == pygame.K_RIGHT and self.lumberjack_on_left:
                    self._flip_lumberjack(flip_direction=1)
                    self.lumberjack_on_left = False

    def _flip_lumberjack(self, flip_direction: int):
        # flip_direction wynoszące 1 oznacza przejście na prawo, a -1 w lewo
        self.lumberjack_ready.flip(True, False)
        self.lumberjack_hit.flip(True, False)
        self.lumberjack_ready.x += flip_direction * 3.44 * self.trunk.rect.width
        self.lumberjack_ready.rect.x = self.lumberjack_ready.x
        self.lumberjack_hit.x += flip_direction * 2 * self.trunk.rect.width
        self.lumberjack_hit.rect.x = self.lumberjack_hit.x

    def _check_keyup_events(self, event):
        if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
            self.hit = False

    def get_all_branches(self):
        return self.branches_left + self.branches_right

    def _change_fullscreen(self):
        if self.settings.fullscreen:
            self.settings.fullscreen = False
            surface_size = self.screen.get_size()
            self.screen = pygame.display.set_mode(
                (self.settings.screen_width, self.settings.screen_height),
                pygame.RESIZABLE)
            self.screen_width = self.screen.get_width()
            self.screen_height = self.screen.get_height()

            self._scale_to(self.scalable, surface_size, (self.settings.screen_width, self.settings.screen_height))
            self._scale_to(self.get_all_branches(), surface_size,
                           (self.settings.screen_width, self.settings.screen_height))
            self.font = pygame.font.Font('fonts/bungee-regular.ttf',
                                         int(50 * (self.screen_width / self.settings.screen_width))) # Czy to potrzebne?

        else:
            self.settings.fullscreen = True
            surface_size = self.screen.get_size()
            self.screen = pygame.display.set_mode(
                (self.settings.fullscreen_width, self.settings.fullscreen_height), pygame.FULLSCREEN)
            self.screen_width = self.screen.get_width()
            self.screen_height = self.screen.get_height()
            self._scale_to(self.scalable, surface_size,
                           (self.settings.fullscreen_width, self.settings.fullscreen_height))
            self._scale_to(self.get_all_branches(), surface_size,
                           (self.settings.fullscreen_width, self.settings.fullscreen_height))
        self.bee.set_screen(self.screen)
        self.font = pygame.font.Font('fonts/bungee-regular.ttf',
                                     int(50 * (self.screen_width / self.settings.screen_width)))

    def _scale_to(self, objects: list, old_size, new_size, change_pos=True):
        for obj in objects:
            obj.scale(old_size, new_size, change_pos)

    def _create_branches(self):
        for _ in range(self.settings.branch_count):
            start_point = self.settings.branch_start_height_scale * self.screen_height
            step = self.settings.branch_step_scale * self.screen_height
            rand = random.randint(0, 2)
            if rand == 0:
                self.branches.append(None)
            elif rand == 1:
                self.branches.append((self.branches_left[self.last_taken_left], 'left'))
                self.last_taken_left += 1
            elif rand == 2:
                self.branches.append((self.branches_right[self.last_taken_right], 'right'))
                self.last_taken_right += 1
            for i, branch in enumerate(self.branches):
                if branch is None:
                    continue
                branch[0].y = start_point - i * step
                branch[0].rect.y = branch[0].y
            self.top = start_point - len(self.branches) * step
        self._scale_to(self.get_all_branches(), (self.settings.bg_width, self.settings.bg_height),
                       (self.settings.screen_width, self.settings.screen_height),
                       change_pos=False)

    def _add_branch(self):
        rand = random.randint(0, 2)
        if rand == 0:
            self.branches.append(None)
        elif rand == 1:
            if self.last_taken_left == self.settings.branch_count:
                self.last_taken_left = 0
            self.branches_left[self.last_taken_left].y = self.top
            self.branches_left[self.last_taken_left].rect.y = self.branches_left[self.last_taken_left].y
            self.branches.append((self.branches_left[self.last_taken_left], 'left'))
            self.last_taken_left += 1
        elif rand == 2:
            if self.last_taken_right == self.settings.branch_count:
                self.last_taken_right = 0
            self.branches_right[self.last_taken_right].y = self.top
            self.branches_right[self.last_taken_right].rect.y = self.branches_right[self.last_taken_right].y
            self.branches.append((self.branches_right[self.last_taken_right], 'right'))
            self.last_taken_right += 1

    def _create_branch(self, left=True):
        if left:
            branch = BranchProvider(self, 'konar_lewy.png',
                                    position=(self.settings.branch_scale_left * self.screen_width, 100))
        else:
            branch = BranchProvider(self, 'konar_prawy.png',
                                    position=(self.settings.branch_scale_right * self.screen_width, 100))
        return branch

    def _recalculate_screen(self):
        self.screen_width = self.screen.get_width()
        self.screen_height = self.screen.get_height()
        start_point = self.settings.branch_start_height_scale * self.screen_height
        step = self.settings.branch_step_scale * self.screen_height
        self.top = start_point - len(self.branches) * step

    def _hit_tree(self):
        self._recalculate_screen()
        self._add_branch()
        for branch in self.branches:
            if branch is not None:
                branch[0].y += self.settings.branch_step_scale * self.screen_height
                branch[0].rect.y = branch[0].y
        self.branches.pop(0)

    def _check_lumberjack_branch_collision(self, key):
        last = self.branches[0]
        if last is None:
            return False
        if last[1] == 'left' and key == 'left':
            return True
        if last[1] == 'right' and key == 'right':
            return True
        return False

    def _game_over(self, msg):
        self.stats.game_active = False
        self.lose_text = self.font.render(msg, True, self.settings.text_color)
        self.lose_text_rect = self.lose_text.get_rect()
        self.lose_text_rect.center = (self.screen_width / 2, self.screen_height / 2)
        self.screen.blit(self.lose_text, self.lose_text_rect)

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
            self.bee.sound.play(2)
        self.bee.update()

    def _update_slice_wood(self, pos):
        self.slice_wood.set_position(pos)

    def _update_timer(self):
        self.timer.update()
        self.timer.prep_timer()
        if self.stats.time_left < 0 and not self.collision:
            self.stats.time_left = 0
            self.collision = True
            self.timer.timeout = True

    def _update_screen(self):
        self.screen.fill(self.settings.bg_color)
        self.background.blit_me()
        if not self.stats.game_active and not self.collision:

            self.intro_text = self.font.render("The Lumberjack", True, self.settings.text_color)
            self.intro_text_rect = self.intro_text.get_rect()
            self.intro_text_rect.center = (self.screen_width / 2, 100)
            self.screen.blit(self.intro_text, self.intro_text_rect)

            self.enter_text = self.font.render("Press Enter to start", True, self.settings.text_color)
            self.enter_text_rect = self.enter_text.get_rect()
            self.enter_text_rect.center = (self.screen_width / 2, self.screen_height / 2)
            self.screen.blit(self.enter_text, self.enter_text_rect)
        elif not self.text_editor_mode and self.hs.name:
            self.hs.draw()
        else:
            for cloud in self.clouds:
                cloud.blit_me()
            self.bee.blit_me()

            if self.hit:
                self.trunk_base.blit_me()
                self.slice_wood.blit_me()
                self.trunk.blit_me()
                if not self.collision:
                    self.lumberjack_hit.blit_me()
            else:
                self.tree.blit_me()
                if not self.collision:
                    self.lumberjack_ready.blit_me()

            for branch in self.branches:
                if branch is not None:
                    branch[0].blit_me()

            if self.collision:
                self.stats.game_active = False
                if self.timer.timeout:
                    self._game_over("Timeout")
                else:
                    self._game_over("Crushed")
                self.grave.blit_me()
                if self.hs.check_highscores_list():
                    self.hs.show_player_name()
                    self.text_editor_mode = True

            self.sb.show_score()
            self.timer.draw()
        pygame.display.flip()
        self.clock.tick(self.settings.FPS)


if __name__ == '__main__':
    lj = LumberjackGame()
    lj.run_game()
