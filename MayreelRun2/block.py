from pico2d import *


class Block:
    image = None

    def __init__(self, x, y):
        if Block.image == None:
            self.image = load_image('map/mayreel_block_ground1_400.png')
        self.x = x  # 블럭 좌표로 나타냄
        self.y = y
        self.col_left = self.x - 50
        self.col_bottom = self.y - 50
        self.col_right = self.x + 50
        self.col_top = self.y + 50
        self.font = load_font('ENCR10B.TTF', 16)

    def update(self):
        pass

    def draw(self):
        self.image.clip_draw(0, 0, self.image.w, self.image.h, self.x, self.y, 100, 100)
        draw_rectangle(self.col_left, self.col_bottom, self.col_right, self.col_top)
        #self.font.draw(self.x - 60, self.y + 30, '(x: %3.2f)' % self.x, (255, 255, 0))
