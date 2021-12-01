from pico2d import *

import game_framework
import game_world

TIME_PER_ACTION = 1
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 16


class Missile:
    image = None

    def __init__(self, x, y):
        if Missile.image is None:
            self.image_start = load_image('effect/missile/missile_start.png')
            self.image_loop = load_image('effect/missile/missile_loop.png')
            self.image_end = load_image('effect/missile/missile_end.png')
        self.x = x
        self.y = y

    def update(self):
        pass
    def draw(self):
        pass