from pico2d import *

import game_framework

class Sky:
    def __init__(self):
        self.image = load_image('map/background_sky.png')

    def update(self):
        pass

    def draw(self):
        self.image.clip_draw(0, 0, 32, 64, 800, 450, 1600, 900)