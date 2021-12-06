import random

import pygame
from pygame.sprite import Sprite


class LandscapeBaseClass(Sprite):
    def __init__(self, lj_game, image, position: tuple = (0, 0)):
        super(LandscapeBaseClass, self).__init__()
        self.screen = lj_game.screen
        self.screen_rect = lj_game.screen.get_rect()
        self.screen_width = self.screen_rect.width
        self.screen_height = self.screen_rect.height

        self.settings = lj_game.settings

        self.original_image = pygame.image.load(f'images/{image}')
        self.image = pygame.image.load(f'images/{image}')
        self.rect = self.image.get_rect()

        self.flipped_x = False
        self.flipped_y = False

        self.rect.x = position[0]
        self.rect.y = position[1]

        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def blit_me(self):
        self.screen.blit(self.image, self.rect)

    def scale(self, old_size: tuple, new_size: tuple, change_pos=True):
        k_x = new_size[0] / old_size[0]
        k_y = new_size[1] / old_size[1]

        new_width = int(self.rect.width * k_x)
        new_height = int(self.rect.height * k_y)

        old_x = self.x
        old_y = self.y

        self.image = pygame.transform.scale(self.original_image, (new_width, new_height))
        self.image = pygame.transform.flip(self.image, self.flipped_x, self.flipped_y)
        self.rect = self.image.get_rect()

        self.x = old_x
        self.y = old_y

        self.rect.x = self.x
        self.rect.y = self.y

        if change_pos:
            self.x *= k_x
            self.y *= k_y
            self.rect.x = self.x
            self.rect.y = self.y

    def flip(self, flip_x, flip_y):
        if flip_x:
            self.flipped_x = not self.flipped_x
        if flip_y:
            self.flipped_y = not self.flipped_y
        self.image = pygame.transform.flip(self.image, flip_x, flip_y)

    def set_position(self, position):
        self.rect.x = position[0]
        self.rect.y = position[1]
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def set_screen(self, screen):
        self.screen = screen
        self.screen_width = self.screen.get_width()
        self.screen_height = self.screen.get_height()


class Cloud(LandscapeBaseClass):
    def __init__(self, lj_game, image, cloud_number, position: tuple = (0, 0)):
        super(Cloud, self).__init__(lj_game, image, position)
        self.cloud_number = cloud_number


class Bee(LandscapeBaseClass):
    def __init__(self, lj_game, image, position: tuple = (0, 0)):
        super(Bee, self).__init__(lj_game, image, position)

        self.overflow = int(100 * (self.screen_width / 500))
        self.sound = pygame.mixer.Sound('sounds/bee.wav')

    def check_edges(self):
        if self.rect.x > self.screen_width + 2 * self.overflow or self.rect.x < -2 * self.overflow:
            return True

    def update(self):
        self.x += (self.settings.bee_speed * (self.screen_width / self.settings.bg_width) * self.settings.bee_direction)
        self.rect.x = self.x

    def change_height(self):
        self.y = random.randint(100, self.screen_height - 100)
        self.rect.y = self.y


class Tree(LandscapeBaseClass):
    def __init__(self, lj_game, image, position: tuple = (0, 0)):
        super(Tree, self).__init__(lj_game, image, position)


class Lumberjack(LandscapeBaseClass):
    def __init__(self, lj_game, image, position: tuple = (0, 0)):
        super(Lumberjack, self).__init__(lj_game, image, position)


class BranchProvider(LandscapeBaseClass):
    def __init__(self, lj_game, image, position: tuple = (0, 0)):
        super(BranchProvider, self).__init__(lj_game, image, position)
