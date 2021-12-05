from pico2d import *

import server


class Block:
    image = None

    def __init__(self, x, y, code):
        if Block.image is None:
            self.image = [load_image('map/mayreel_block_ground1_400.png'),
                          load_image('map/mayreel_block_ground2_400.png'),
                          load_image('map/mayreel_block_ground3_400.png')]

        self.x = x  # 블럭 좌표로 나타냄
        self.y = y
        self.code = code
        self.col_left = self.x - 50
        self.col_bottom = self.y - 50
        self.col_right = self.x + 50
        self.col_top = self.y + 50
        self.state = 'awake'

    def get_col(self):
        return self.x - 50, self.y - 50, self.x + 50, self.y + 50

    def update(self):
        pass

    def block_update(self):
        if self.state == 'sleep':
            if server.player is not None and abs(self.x - server.player.x) <= 1500 and abs(
                    self.y - server.player.y) <= 1000:
                self.state = 'awake'
                server.block.append(self)
                server.block_sleep.remove(self)

        elif self.state == 'awake':
            if server.player is None or abs(self.x - server.player.x) > 1500 and abs(self.y - server.player.y) > 1000:
                self.state = 'sleep'
                server.block_sleep.append(self)
                server.block.remove(self)

    def draw(self):
        self.image[self.code].clip_draw(0, 0, self.image[self.code].w, self.image[self.code].h, self.x + server.cx,
                                        self.y + server.cy, 100, 100)
        # draw_rectangle(self.col_left, self.col_bottom, self.col_right, self.col_top)
        """self.font.draw(self.x - 60 + server.cx, self.y + server.cy + 30,
                       '(%.2f,%.2f)' % (self.x + server.cx, self.y + server.cy), (255, 255, 0))"""
