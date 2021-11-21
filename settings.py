import random

import pygame
from screeninfo import get_monitors


class Settings:
    def __init__(self):
        self.screen_width = 800
        self.screen_height = 450
        self.fullscreen = False

        self.bg_width = 1920
        self.bg_height = 1080

        monitor = get_monitors()[0]
        self.fullscreen_width = monitor.width
        self.fullscreen_height = monitor.height

        self.bg_color = (150, 150, 0)
        self.FPS = 60

        self.number_of_clouds = 4
        self.cloud_speed = [random.uniform(0.2, 1) for _ in range(self.number_of_clouds)]

        self.bee_speed = 10
        self.bee_direction = -1

        self.branch_count = 10
        self.branch_step_scale = 0.25
        self.branch_start_height_scale = 0.55

        self.slice_wood_scale = 900 / self.bg_height
        self.lumberjack_scale = 1040 / self.bg_height
        self.branch_scale_left = 447 / self.bg_width
        self.branch_scale_right = 1037 / self.bg_width