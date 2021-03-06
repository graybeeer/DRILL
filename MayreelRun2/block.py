from pico2d import *

import server


class Block:
    image = None

    def __init__(self, x=0, y=0, code=0):
        if Block.image is None:
            self.image = [load_image('map/mayreel_block_ground1_400.png'),
                          load_image('map/mayreel_block_ground2_400.png'),
                          load_image('map/mayreel_block_ground3_400.png'),
                          load_image('map/mayreel_block_blick_1_400.png'),
                          load_image('map/mayreel_block_blick_2_400.png'),
                          load_image('map/pipe_1.png'),
                          load_image('map/pipe_2.png'),
                          load_image('map/pipe_3.png'),
                          load_image('map/Mayreel_Block_question_400.png'),
                          load_image('map/Mayreel_Block_question_used_400.png'),
                          load_image('map/Mayreel_Block_flag_1_400.png'),
                          load_image('map/Mayreel_Block_flag_2_400.png'),
                          load_image('map/Mayreel_Block_flag_3_400.png'),]

        self.font = load_font('ENCR10B.TTF', 16)
        self.x = x  # 블럭 좌표로 나타냄
        self.y = y
        self.code = code
        self.col_left = self.x - 50
        self.col_bottom = self.y - 50
        self.col_right = self.x + 50
        self.col_top = self.y + 50
        for i in range(server.map_area_x):
            for j in range(server.map_area_y):
                if server.map_area_size_x * i <= x < server.map_area_size_x * (i + 1):
                    if server.map_area_size_y * j <= y < server.map_area_size_x * (j + 1):
                        self.area_x = i
                        self.area_y = j
        self.state = 'awake'

    def block_update(self):
        if self.state == 'sleep':
            if abs(server.player_area_x - self.area_x) <= 1 and abs(server.player_area_y - self.area_y) <= 1:
                self.state = 'awake'
                server.block.append(self)
                server.block_sleep.remove(self)

        elif self.state == 'awake':
            if abs(server.player_area_x - self.area_x) > 1 or abs(server.player_area_y - self.area_y) > 1:
                self.state = 'sleep'
                server.block_sleep.append(self)
                server.block.remove(self)

    def get_col(self):
        return self.x - 50, self.y - 50, self.x + 50, self.y + 50

    def update(self):
        pass

    def draw(self):
        if self.state == 'awake':
            self.image[self.code].clip_draw(0, 0, self.image[self.code].w, self.image[self.code].h, self.x + server.cx,
                                            self.y + server.cy, 100, 100)
        # draw_rectangle(self.col_left, self.col_bottom, self.col_right, self.col_top)
        # self.font.draw(self.x - 60 + server.cx, self.y + server.cy + 30, '(%.3f,%.3f)' % (self.area_x, self.area_y),(255, 255, 0))
        # self.font.draw(self.x - 60 + server.cx, self.y + server.cy, '(%s)' % (self.state),(255, 255, 0))

    # 저장할 정보를 선택하는 함수
    def __getstate__(self):
        state = {'x': self.x, 'y': self.y, 'code': self.code, 'col_left': self.col_left, 'col_bottom': self.col_bottom,
                 'col_right': self.col_right, 'col_top': self.col_top, 'area_x': self.area_x, 'area_y': self.area_y}
        return state

    # 정보를 복구하는 함수
    def __setstate__(self, state):
        self.__init__()
        self.__dict__.update(state)
