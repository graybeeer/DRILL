from pico2d import *

import server


class Background:
    image = None

    def __init__(self, x=0, y=0, code=0):
        if Background.image is None:
            self.image = [load_image('map/mayreel_block_grass_1_400.png'),
                          load_image('map/mayreel_block_grass_3_400.png'),
                          load_image('map/Mayreel_Block_cloud_400.png'),
                          load_image('map/Mayreel_mountain.png')]

        self.x = x  # 블럭 좌표로 나타냄
        self.y = y
        self.code = code
        for i in range(server.map_area_x):
            for j in range(server.map_area_y):
                if server.map_area_size_x * i <= x < server.map_area_size_x * (i + 1):
                    if server.map_area_size_y * j <= y < server.map_area_size_x * (j + 1):
                        self.area_x = i
                        self.area_y = j
        self.state = 'awake'

    def background_update(self):
        if self.state == 'sleep':
            if abs(server.player_area_x - self.area_x) <= 1 and abs(server.player_area_y - self.area_y) <= 1:
                if self in server.block_sleep:
                    self.state = 'awake'
                    server.block.append(self)
                    server.block_sleep.remove(self)

        elif self.state == 'awake':
            if abs(server.player_area_x - self.area_x) > 1 or abs(server.player_area_y - self.area_y) > 1:
                if self in server.block:
                    self.state = 'sleep'
                    server.block_sleep.append(self)
                    server.block.remove(self)

    def update(self):
        pass

    def draw(self):
        if self.state == 'awake':
            self.image[self.code].clip_draw(0, 0, self.image[self.code].w, self.image[self.code].h, self.x + server.cx,
                                            self.y + server.cy + self.image[self.code].h / 2)

    # 저장할 정보를 선택하는 함수
    def __getstate__(self):
        state = {'x': self.x, 'y': self.y, 'code':self.code, 'area_x': self.area_x, 'area_y': self.area_y}
        return state

    # 정보를 복구하는 함수
    def __setstate__(self, state):
        self.__init__()
        self.__dict__.update(state)
