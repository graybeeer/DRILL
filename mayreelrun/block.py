import game_framework
import game_world
from pico2d import *


class Block:
    def __init__(self, x, y):
        self.image = load_image('map/mayreel_block_ground1_400.png')
        self.x = x  # 블럭 좌표로 나타냄
        self.y = y
        self.col_rect = [self.x - self.image.w / 2, self.y - self.image.h / 2,
                         self.x + self.image.w / 2, self.y + self.image.h / 2]

    def get_bb(self):
        return self.x - self.image.w / 2, self.y - self.image.h / 2, self.x + self.image.w / 2, self.y + self.image.h / 2

    def update(self):
        pass

    def draw(self):
        self.image.clip_draw(0, 0, self.image.w, self.image.h, self.x, self.y)
        draw_rectangle(*self.get_bb())
