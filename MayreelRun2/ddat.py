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
        if server.player is not None and abs(ddat.x - server.player.x) <= 1500 and abs(ddat.y - server.player.y) <= 1000:
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
        if server.player is None or abs(ddat.x - server.player.x) > 1500: # 조건 불충족시 작동 멈춤
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

    def __init__(self, x, y):
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
        self.dir = 1  # 플레이어 방향
        self.velocity = 0  # 플레이어 속도 양수 오른쪽 음수 왼쪽

        self.frame = 0
        # ---------------------------------------------- 플레이어 상태
        self.event_que = []
        self.cur_state = SleepState
        self.cur_state.enter(self, None)

    def get_col_feet(self):
        return self.x - 30, self.y - 80, self.x + 34, self.y - 60

    def add_event(self, event):
        self.event_que.insert(0, event)

    def update(self):
        self.cur_state.do(self)
        if len(self.event_que) > 0:
            event = self.event_que.pop()
            self.cur_state.exit(self, event)
            self.cur_state = next_state_table[self.cur_state][event]
            self.cur_state.enter(self, event)
        pass

    def draw(self):
        self.cur_state.draw(self)
        pass
