from pico2d import *

import server


class Startpoint:
    def __init__(self, x=0, y=0):
        self.image = load_image('map/mayreel_idle_0_400.png')
        self.x = x
        self.y = y
        self.state = 'awake'

    def start(self):
        server.player_start_x = self.x
        server.player_start_y = self.y - 24
        if self.state == 'awake':
            self.state = 'sleep'
        else:
            self.state = 'awake'
        pass

    def update(self):
        pass

    def draw(self):
        if self.state == 'awake':
            self.image.clip_draw(0, 0, self.image.w, self.image.h, self.x + server.cx, self.y + server.cy, 128, 128)
        pass

    # 저장할 정보를 선택하는 함수
    def __getstate__(self):
        state = {'x': self.x, 'y': self.y}
        return state

    # 정보를 복구하는 함수
    def __setstate__(self, state):
        self.__init__()
        self.__dict__.update(state)
