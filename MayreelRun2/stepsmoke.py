from pico2d import *

import game_framework
import game_world

TIME_PER_ACTION = 1
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 16


class Stepsmoke:
    image = None

    def __init__(self, x, y):
        if Stepsmoke.image is None:
            self.image = [load_image('effect/step/StepSmoke_0.png'),
                          load_image('effect/step/StepSmoke_1.png'),
                          load_image('effect/step/StepSmoke_2.png'),
                          load_image('effect/step/StepSmoke_3.png'),
                          load_image('effect/step/StepSmoke_4.png'),
                          load_image('effect/step/StepSmoke_5.png'),
                          load_image('effect/step/StepSmoke_6.png'),
                          load_image('effect/step/StepSmoke_7.png'),
                          load_image('effect/step/StepSmoke_8.png')]
        self.x = x
        self.y = y
        self.frame = 0
        self.size = 1  # 1이 100%

    def update(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time)
        if int(self.frame) >= 9:
            game_world.remove_object(self)
        pass

    def draw(self):
        if int(self.frame) == 0 or int(self.frame) == 8:
            self.size = 0.2
        elif int(self.frame) == 1 or int(self.frame) == 7:
            self.size = 0.3
        elif int(self.frame) == 2 or int(self.frame) == 6:
            self.size = 0.4
        elif int(self.frame) == 3 or int(self.frame) == 5:
            self.size = 0.5
        elif int(self.frame) == 4:
            self.size = 0.5

        self.image[int(self.frame)].clip_draw(0, 0, self.image[int(self.frame)].w, self.image[int(self.frame)].h,
                                              self.x, self.y, self.image[int(self.frame)].w * self.size,
                                              self.image[int(self.frame)].h * self.size)
