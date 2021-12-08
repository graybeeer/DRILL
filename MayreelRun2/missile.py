from pico2d import *

import game_framework
import game_world
import server

TIME_PER_ACTION = 1
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 10


class Missile:
    image = None

    def __init__(self):
        if Missile.image is None:
            self.image_start = load_image('effect/missile/missile_start.png')
            self.image_loop = load_image('effect/missile/missile_loop.png')
            self.image_end = load_image('effect/missile/missile_end.png')
        self.x = server.player.x + 50 * server.player.dir
        self.y = server.player.y
        self.frame = 0
        self.state = 0

    def update(self):
        self.x = server.player.x + 50 * server.player.dir
        self.y = server.player.y
        if self.state == 0:
            self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time)
            if int(self.frame) > 6:
                self.state = 1
                self.frame = 0
        elif self.state == 1:
            self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time)
            if int(self.frame) > 6:
                self.state = 2
                self.frame = 0
                bullet = Bullet(self.x, self.y, server.player.dir)
                game_world.add_object(bullet, 4)
        elif self.state == 2:
            self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time)
            if int(self.frame) > 6:
                game_world.remove_object(self)
                server.missile = None

    def draw(self):
        if self.state == 0:
            self.image_start.clip_draw(192 * int(clamp(0, self.frame, 6)), 0, 192, 192, self.x + server.cx,
                                       self.y + server.cy, 192, 192)
        if self.state == 1:
            self.image_loop.clip_draw(192 * int(clamp(0, self.frame, 6)), 0, 192, 192, self.x + server.cx,
                                      self.y + server.cy, 192, 192)
        if self.state == 2:
            self.image_end.clip_draw(192 * int(clamp(0, self.frame, 6)), 0, 192, 192, self.x + server.cx,
                                     self.y + server.cy, 192, 192)
        pass


class Bullet:
    image = None

    def __init__(self, x, y, dir):
        if Bullet.image is None:
            self.image = load_image('effect/missile/missile_bullet.png')
        self.x = x
        self.y = y
        self.dir = dir

    def update(self):
        self.x += 500 * game_framework.frame_time
        if self.x>10000:
            game_world.remove_object(self)

    def draw(self):
        self.image.clip_draw(0, 0, self.image.w, self.image.h, self.x + server.cx, self.y + server.cy)
