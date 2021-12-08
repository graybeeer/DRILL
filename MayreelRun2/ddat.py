import random

from pico2d import *

import game_world
import collision
import game_framework
import server
from BehaviorTree import BehaviorTree, SelectorNode, SequenceNode, LeafNode

PIXEL_PER_METER = (10.0 / 1)  # 10 pixel 10 cm
RUN_SPEED_KMPH = 30  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

TIME_PER_ACTION = 1.0
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 16
SHOT_FRAMES_PER_ACTION = 20


class Ddat:
    image = None

    def __init__(self, x=0, y=0):
        if Ddat.image is None:
            self.image = load_image('ddat/DDAT_400.png')
            self.image_idle = load_image('ddat/idle/idle.png')
            self.image_walk = load_image('ddat/walk/walk.png')
            self.image_run = load_image('ddat/run/run.png')
        self.x = x
        self.y = y
        self.col_left = self.x - 30
        self.col_bottom = self.y - 80
        self.col_right = self.x + 34
        self.col_top = self.y + 64
        self.gravity = 0  # 중력
        self.gravity_tic = 1000  # 프레임당 추가되는 중력
        self.gravity_max = 700  # 최대 중력
        self.jump_power = 0  # 점프 힘
        self.jump_power_tic = 1000  # 프레임당 줄어드는 점프힘
        self.jump_power_max = 1000  # 점프 힘 최대
        for i in range(server.map_area_x):
            for j in range(server.map_area_y):
                if server.map_area_size_x * i <= x < server.map_area_size_x * (i + 1):
                    if server.map_area_size_y * j <= y < server.map_area_size_x * (j + 1):
                        self.area_x = i
                        self.area_y = j
        self.state_before = 'idle'
        self.state = 'idle'
        self.state_sleep = 'awake'
        self.state_editor = True
        self.dir = 0  # 이동 방향
        self.velocity = 0  # 이동 속도 양수 오른쪽 음수 왼쪽
        self.timer = 1.0  # change direction every 1 sec when wandering
        self.frame = 0
        self.frame_max = 1
        self.build_behavior_tree()
        # ---------------------------------------------- 플레이어 상태

    def wander(self):
        self.timer -= game_framework.frame_time
        """for block in server.block:
            if collision.collide(self.get_col_feet_future(), block.get_col()):
                pass
            if block == server.block[len(server.block) - 1]:
                self.dir *= -1"""
        if self.timer < 0:
            self.timer += 1.0
            self.velocity = random.randint(-1, 1) * RUN_SPEED_PPS
        return BehaviorTree.SUCCESS

    def find_player(self):
        if server.player is not None:
            distance = (server.player.x - self.x) ** 2 + (server.player.y - self.y) ** 2
            if distance < 500 ** 2:
                if (server.player.x - self.x) > 0:
                    self.dir = 1
                else:
                    self.dir = -1
                return BehaviorTree.SUCCESS
            else:
                self.velocity = 0
                return BehaviorTree.FAIL

    def move_to_player(self):
        self.velocity = self.dir * RUN_SPEED_PPS
        return BehaviorTree.SUCCESS

    def build_behavior_tree(self):
        wander_node = LeafNode("Wander", self.wander)
        find_player_node = LeafNode("Find Player", self.find_player)
        move_to_player_node = LeafNode("Move to Player", self.move_to_player)
        chase_node = SequenceNode("Chase")
        chase_node.add_children(find_player_node, move_to_player_node)
        wander_chase_node = SelectorNode("WanderChase")
        wander_chase_node.add_children(chase_node, wander_node)
        self.bt = BehaviorTree(wander_chase_node)

    def get_col_feet(self):
        return self.x - 30, self.y - 80, self.x + 34, self.y - 60

    def get_col_body_left(self):
        return self.x - 50, self.y - 70, self.x - 30, self.y + 60

    def get_col_body_right(self):
        return self.x + 30, self.y - 70, self.x + 50, self.y + 60

    def get_col_head(self):
        return self.x - 30, self.y + 44, self.x + 34, self.y + 64

    def get_col_feet_future(self):
        return self.x - 30 + self.velocity * game_framework.frame_time * 1, self.y - 80, self.x + 34 + self.velocity * game_framework.frame_time * 1, self.y - 60

    def monster_update(self):
        self.state_editor = False
        if self.state_sleep == 'sleep':
            if abs(server.player_area_x - self.area_x) <= 1 and abs(server.player_area_y - self.area_y) <= 1:
                self.state_sleep = 'awake'
                server.monster.append(self)
                server.monster_sleep.remove(self)

        elif self.state_sleep == 'awake':
            if abs(server.player_area_x - self.area_x) > 1 or abs(server.player_area_y - self.area_y) > 1:
                self.state_sleep = 'sleep'
                server.monster_sleep.append(self)
                server.monster.remove(self)

    def update(self):
        if self.state_editor == False:
            self.bt.run()
            self.state_check()
            self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % self.frame_max
            self.jump_gravity()
            self.x += self.velocity * game_framework.frame_time
            self.y -= self.gravity * game_framework.frame_time
            self.y += self.jump_power * game_framework.frame_time
            self.landing_feet_head()
            self.block_collide_left()
            self.block_collide_right()
            self.x = clamp(30, self.x, server.map_area_size_x * server.map_area_x - 34)  # 플레이어 위치 제한
            self.y = clamp(-500, self.y, server.map_area_size_y * server.map_area_y - 64)
            if self.y<-300:
                game_world.remove_object(self)
        pass

    def state_check(self):
        if self.velocity != 0:
            self.state = 'walk'
            self.frame_max = 11
        else:
            self.state = 'idle'
            self.frame_max = 14
        if self.state != self.state_before:
            self.frame = 0
            self.state_before = self.state

    def jump_gravity(self):
        if self.gravity < self.gravity_max:  # 최대까지 중력 증가
            self.gravity += self.gravity_tic * game_framework.frame_time
        elif self.gravity >= self.gravity_max:
            self.gravity = self.gravity_max
        if self.jump_power > 0:
            self.jump_power -= self.jump_power_tic * game_framework.frame_time
            if self.jump_power <= 0:
                self.jump_power = 0

    def landing_feet_head(self):
        for block in server.block:
            if collision.collide(self.get_col_feet(), block.get_col()) and (
                    self.jump_power - self.gravity) <= 0:
                self.y = 80 + block.col_top
                self.gravity = 0
                self.jump_power = 0
                break
            elif collision.collide(self.get_col_head(), block.get_col()) and (
                    self.jump_power - self.gravity) > 0:
                self.y = -64 + block.col_bottom
                self.jump_power = 0
                break

    def block_collide_left(self):
        for block in server.block:
            if collision.collide(self.get_col_body_left(), block.get_col()):
                self.x = 50 + block.col_right

    def block_collide_right(self):
        for block in server.block:
            if collision.collide(self.get_col_body_right(), block.get_col()):
                self.x = -50 + block.col_left

    def draw(self):
        if self.state_sleep == 'sleep':
            pass
        elif self.state_editor == True:
            self.image.clip_composite_draw(0, 0, 256, 256, 0, '', self.x + server.cx, self.y + server.cy)
        elif self.state == 'idle':
            if self.dir > 0:
                self.image_idle.clip_composite_draw(int(self.frame) * 256, 0, 256, 256, 0, '', self.x + server.cx,
                                                    self.y + server.cy, 256, 256)
            else:
                self.image_idle.clip_composite_draw(int(self.frame) * 256, 0, 256, 256, 0, 'h', self.x + server.cx + 4,
                                                    self.y + server.cy, 256, 256)
        elif self.state == 'walk':
            if self.dir > 0:
                self.image_walk.clip_composite_draw(int(self.frame) * 256, 0, 256, 256, 0, '', self.x + server.cx,
                                                    self.y + server.cy, 256, 256)
            else:
                self.image_walk.clip_composite_draw(int(self.frame) * 256, 0, 256, 256, 0, 'h', self.x + server.cx + 4,
                                                    self.y + server.cy, 256, 256)
        pass

    # 저장할 정보를 선택하는 함수
    def __getstate__(self):
        state = {'x': self.x, 'y': self.y, 'col_left': self.col_left, 'col_bottom': self.col_bottom,
                 'col_right': self.col_right, 'col_top': self.col_top, 'area_x': self.area_x, 'area_y': self.area_y}
        return state

    # 정보를 복구하는 함수
    def __setstate__(self, state):
        self.__init__()
        self.__dict__.update(state)
