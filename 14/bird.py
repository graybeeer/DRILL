import game_framework
from pico2d import *
import random

PIXEL_PER_METER = (10.0 / 0.3)  # 10픽셀당 30cm
RUN_SPEED_KMPH = 50.0  # Km / Hour 시속50km
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)  # 프레임당 움직이는 속도

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 15  # 한 프레임당 걸리는 시간 결정


class Bird:

    def __init__(self, w, h):
        self.x, self.y = random.randint(50, 1600 - 50), random.randint(300, 500)  # 새의 x좌표는 화면 맨 왼쪽에서 끝까지 랜덤
        self.w = w  # main_state에서 크기를 받아서 새 크기 결정
        self.h = h
        self.frame = 0
        self.image = load_image('bird100x100x14.png')  # 새 이미지
        self.dir = random.choice([1, -1])  # 새의 시작 방향은 왼쪽 오른쪽 랜덤

    def update(self):
        if self.dir == 1:
            self.x += RUN_SPEED_PPS * game_framework.frame_time  # 속도 x 델타타임
        elif self.dir == -1:
            self.x -= RUN_SPEED_PPS * game_framework.frame_time

        self.x = clamp(50, self.x, 1600 - 50)  # 새의 이동반경은 화면 안으로 고정
        if self.x <= 50 and self.dir == -1:  # 만약 왼쪽으로 가는 상태에서 왼쪽벽에 부딪히면
            self.dir = 1  # 오른쪽으로 이동방향 변경
        elif self.x >= 1600 - 50 and self.dir == 1:  # 반대 방향도 마찬가지
            self.dir = -1
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 14
        # 프레임속도에 따라 프레임 변경 총 14프레임
        pass

    def draw(self):
        if self.dir == 1:  # 오른쪽으로 갈때랑 왼쪽으로 갈때 이미지 출력 좌우변경
            self.image.clip_composite_draw(int(self.frame) * 100, 0, 100, 100, 0, '', self.x, self.y, self.w, self.h)
        elif self.dir == -1:
            self.image.clip_composite_draw(int(self.frame) * 100, 0, 100, 100, 0, 'h', self.x, self.y, self.w, self.h)
