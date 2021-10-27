import pygame
from pygame.sprite import Sprite


class Landscape(Sprite):
    def __init__(self, lj_game, image):
        super(Landscape, self).__init__()
        self.screen = lj_game.screen
        self.screen_rect = lj_game.screen.get_rect()
        self.settings = lj_game.settings

        self.original_image = pygame.image.load(f'images/{image}')
        self.image = pygame.image.load(f'images/{image}')
        self.rect = self.image.get_rect()

    def blit_me(self):
        self.screen.blit(self.image, self.rect)

    def scale(self, old_size: tuple, new_size: tuple):
        k_x = new_size[0] / old_size[0]
        k_y = new_size[1] / old_size[1]

        old_x = self.rect.x
        old_y = self.rect.y

        new_width = int(self.rect.width * k_x)
        new_height = int(self.rect.height * k_y)

        self.image = pygame.transform.scale(self.original_image, (new_width, new_height))
        self.rect = self.image.get_rect()
        self.rect.x = old_x
        self.rect.y = old_y


class Cloud(Landscape):
    def __init__(self, lj_game, image, cloud_number):
        super(Cloud, self).__init__(lj_game, image)
        self.cloud_number = cloud_number
        self.rect.topleft = self.screen_rect.topleft
        self.x = float(self.rect.x)
