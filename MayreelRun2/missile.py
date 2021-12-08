from pico2d import *

import collision
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
        self.dis = 0
        self.dir = dir
        self.shot_sound = load_wav('Mayreel/01_mayreel_laser_01.wav')
        self.shot_sound.set_volume(50)
        self.shot_sound.play()

    def update(self):
        self.x += 1000 * game_framework.frame_time * self.dir
        self.dis += 1000 * game_framework.frame_time * self.dir
        for monster in server.monster:  # 미사일이 몬스터와 닿으면
            if collision.collide(self.get_col(), monster.get_col()):
                game_world.remove_object(monster)  # 몬스터 삭제
        if self.dis > 2000:  # 미사일이 맵 끝에 닿으면 스스로 삭제
            game_world.remove_object(self)

    def draw(self):
        self.image.clip_draw(0, 0, self.image.w, self.image.h, self.x + server.cx, self.y + server.cy)

    def get_col(self):
        return self.x - 40, self.y - 40, self.x + 40, self.y + 40


class Cushion:
    image = None

    def __init__(self, x, y):
        if Cushion.image is None:
            self.x = x
            self.y = y
            self.velocity = 200
            self.gravity = 0
            self.gravity_tic = 1000  # 프레임당 추가되는 중력
            self.gravity_max = 700  # 최대 중력
            self.image = load_image('Mayreel/cushion.png')

    def update(self):
        self.gravity_check()
        self.x += self.velocity * game_framework.frame_time
        self.y -= self.gravity * game_framework.frame_time
        self.landing_feet_head()
        self.block_collide_left()
        self.block_collide_right()
        if collision.collide(self.get_col(), server.player.get_col()):
            server.player.shot_chance += 1
            server.player.shot_chance = clamp(0, server.player.shot_chance, server.player.shot_chance_max)
            game_world.remove_object(self)
        if self.x > 10000 or self.x < -300 or self.y > 10000 or self.y < -300:  # 미사일이 맵 끝에 닿으면 스스로 삭제
            game_world.remove_object(self)

    def draw(self):
        self.image.clip_draw(0, 0, self.image.w, self.image.h, self.x + server.cx, self.y + server.cy, 98, 96)

    def get_col(self):
        return self.x - 49, self.y - 48, self.x + 49, self.y - 30

    def get_col_feet(self):
        return self.x - 40, self.y - 40, self.x + 40, self.y

    def get_col_head(self):
        return self.x - 40, self.y, self.x + 40, self.y + 40

    def get_col_body_left(self):
        return self.x - 49, self.y - 40, self.x - 30, self.y + 40

    def get_col_body_right(self):
        return self.x + 30, self.y - 40, self.x + 49, self.y + 40

    def gravity_check(self):
        if self.gravity < self.gravity_max:  # 최대까지 중력 증가
            self.gravity += self.gravity_tic * game_framework.frame_time
        elif self.gravity >= self.gravity_max:
            self.gravity = self.gravity_max

    def landing_feet_head(self):
        for block in server.block:
            if collision.collide(self.get_col_feet(), block.get_col()):
                self.y = 48 + block.col_top
                self.gravity = 0
                # self.jump_power = 0
                break
            """elif collision.collide(self.get_col_head(), block.get_col()) and (
                    self.jump_power - self.gravity) > 0:
                self.y = -self.image.h / 2 + block.col_bottom
                self.jump_power = 0
                break"""

    def block_collide_left(self):
        for block in server.block:
            if collision.collide(self.get_col_body_left(), block.get_col()):
                self.x = 49 + block.col_right
                self.velocity = 200

    def block_collide_right(self):
        for block in server.block:
            if collision.collide(self.get_col_body_right(), block.get_col()):
                self.x = -49 + block.col_left
                self.velocity = -200
