from pico2d import *

# import random
# import game_world
import collision
import game_framework
import server

WAKE, SLEEP, JUMPING, LANDING = range(4)
next_state_table = {}

PIXEL_PER_METER = (10.0 / 0.1)  # 10 pixel 10 cm
RUN_SPEED_KMPH = 10.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

TIME_PER_ACTION = 1.0
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 16
SHOT_FRAMES_PER_ACTION = 20


class SleepState:
    def enter(ddat, event):
        pass

    def exit(ddat, event):
        ddat.frame = 0
        pass

    def do(ddat):
        if server.player is not None:
            ddat.add_event(WAKE)
        pass

    def draw(ddat):
        ddat.image_idle.clip_composite_draw(0, 0, 256, 256, 0, 'h', ddat.x + server.cx + 4,
                                            ddat.y + server.cy, 256, 256)
        pass


class IdleState:
    def enter(ddat, event):
        pass

    def exit(ddat, event):
        ddat.frame = 0
        pass

    def do(ddat):
        if server.player is None: # 조건 불충족시 작동 멈춤
            ddat.add_event(SLEEP)
        ddat.frame = (ddat.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 14
        for block in server.block:
            if collision.collide(ddat.get_col_feet(), block.get_col()):
                break
            if block == server.block[len(server.block) - 1]:
                ddat.add_event(JUMPING)
        pass

    def draw(ddat):
        if ddat.dir > 0:
            ddat.image_idle.clip_composite_draw(int(ddat.frame) * 256, 0, 256, 256, 0, '', ddat.x + server.cx,
                                                ddat.y + server.cy,
                                                256, 256)
        else:
            ddat.image_idle.clip_composite_draw(int(ddat.frame) * 256, 0, 256, 256, 0, 'h', ddat.x + server.cx + 4,
                                                ddat.y + server.cy, 256, 256)
        pass
class LeftWalkState:
    def enter(ddat, event):
        pass

    def exit(ddat, event):
        ddat.frame = 0
        pass

    def do(ddat):
        if server.player is None or abs(ddat.x - server.player.x) > 1500:  # 조건 불충족시 작동 멈춤
            ddat.add_event(SLEEP)
        pass

    def draw(ddat):
        ddat.image_idle.clip_composite_draw(0, 0, 256, 256, 0, 'h', ddat.x + server.cx + 4,
                                            ddat.y + server.cy, 256, 256)
        pass

next_state_table = {
    SleepState: {WAKE: IdleState},
    IdleState: {SLEEP: SleepState, JUMPING: IdleState}
}


class Ddat:
    image = None

    def __init__(self, x=0, y=0):
        if Ddat.image is None:
            self.image_idle = load_image('ddat/idle/idle.png')
            self.image_walk = load_image('ddat/walk/walk.png')
            self.image_run = load_image('ddat/run/run.png')
        self.start_x = x
        self.start_y = x
        self.x = x
        self.y = y
        self.col_left = self.x - 30
        self.col_bottom = self.y - 80
        self.col_right = self.x + 34
        self.col_top = self.y + 64
        for i in range(server.map_area_x):
            for j in range(server.map_area_y):
                if server.map_area_size_x * i <= x < server.map_area_size_x * (i + 1):
                    if server.map_area_size_y * j <= y < server.map_area_size_x * (j + 1):
                        self.area_x = i
                        self.area_y = j
        self.dir = 0  # 플레이어 방향
        self.velocity = 0  # 플레이어 속도 양수 오른쪽 음수 왼쪽

        self.frame = 0
        # ---------------------------------------------- 플레이어 상태
        self.event_que = []
        self.cur_state = SleepState

    def get_col_feet(self):
        return self.x - 30, self.y - 80, self.x + 34, self.y - 60

    def add_event(self, event):
        self.event_que.insert(0, event)
    def monster_update(self):
        if self.state == 'sleep':
            if abs(server.player_area_x - self.area_x) <= 1 and abs(server.player_area_y - self.area_y) <= 1:
                self.state = 'awake'
                server.monster.append(self)
                server.monster_sleep.remove(self)

        elif self.state == 'awake':
            if abs(server.player_area_x - self.area_x) > 1 or abs(server.player_area_y - self.area_y) > 1:
                self.state = 'sleep'
                server.monster_sleep.append(self)
                server.monster.remove(self)
    def update(self):
        self.cur_state.do(self)
        if len(self.event_que) > 0:
            event = self.event_que.pop()
            self.cur_state.exit(self, event)
            if event not in next_state_table[self.cur_state]:  # 다음 키값이 없으면 그대로
                pass
            else:
                self.cur_state = next_state_table[self.cur_state][event]
            self.cur_state.enter(self, event)
        pass

    def draw(self):
        self.cur_state.draw(self)
        pass

    # 저장할 정보를 선택하는 함수
    def __getstate__(self):
        state = {'x': self.x, 'y': self.y, 'col_left': self.col_left, 'col_bottom': self.col_bottom,
                 'col_right': self.col_right, 'col_top': self.col_top, 'area_x': self.area_x, 'area_y': self.area_y, 'cur_state':SleepState}
        return state

    # 정보를 복구하는 함수
    def __setstate__(self, state):
        self.__init__()
        self.__dict__.update(state)