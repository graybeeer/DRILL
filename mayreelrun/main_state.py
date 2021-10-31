from pico2d import *

import game_framework
import title_state

name = "MainState"

sky = None
player = None
block = None
font = None

press_left = False  # 왼쪽키를 누른 상태인지 아닌지
press_right = False  # 오른쪽키를 누른 상태인지 아닌지


class Sky:
    def __init__(self):
        self.image = load_image('background_sky.png')

    def draw(self):
        self.image.clip_draw(0, 0, 32, 64, 400, 300, 800, 600)


class Block:
    def __init__(self):
        self.image = load_image('map/mayreel_block_ground1_400.png')
        self.x = 2  # 블럭 좌표로 나타냄
        self.y = 0
        pass

    def draw(self):
        self.image.clip_draw(0, 0, self.image.w_value(), self.image.h_value(),
                             (2 * self.x + 1) * self.image.w_value() / 2,
                             (2 * self.y + 1) * self.image.h_value() / 2)
        pass


class Player:

    def __init__(self):
        self.status = 'idle'  # idle=멈춘상태 walk= 달리는 상태 jump=공중에 있는 상태 slide=슬라이딩 상태
        self.status_move = 'stop'  # stop=완전히 멈춘 상태 left=왼쪽으로 이동 상태 right=오른쪽으로 이동 상태
        self.status_save = 'idle'  # 바로 전 프레임의 플레이어 상태
        self.x, self.y = 0, 300  # 캐릭터 위치 ( 가운데 아래)
        self.frame = 0  # 캐릭터 프레임
        self.frame_sec = 0  # 캐릭터 프레임 시간이 일정 지날때마다 캐릭터 1 프레임 증가
        self.frame_sec_all = 0  # 캐릭터 1프레임 당 시간
        self.frame_ani = 0  # 캐릭터 애니메이션의 총 프레임
        self.frame_loop = 'loop'  # loop면 애니메이션 반복
        self.run = False  # 달리고 있는지 아닌지 상태
        self.run_speed = 1

        # 배열을 이용해 여러개의 이미지를 하나의 변수에 넣을 수 있다.
        self.image_idle = [load_image('mayreel/idle/idle_00.gif'),
                           load_image('mayreel/idle/idle_01.gif'),
                           load_image('mayreel/idle/idle_02.gif'),
                           load_image('mayreel/idle/idle_03.gif'),
                           load_image('mayreel/idle/idle_04.gif'),
                           load_image('mayreel/idle/idle_05.gif'),
                           load_image('mayreel/idle/idle_06.gif'),
                           load_image('mayreel/idle/idle_07.gif'),
                           load_image('mayreel/idle/idle_08.gif'),
                           load_image('mayreel/idle/idle_09.gif'),
                           load_image('mayreel/idle/idle_10.gif'),
                           load_image('mayreel/idle/idle_11.gif'),
                           load_image('mayreel/idle/idle_12.gif'),
                           load_image('mayreel/idle/idle_13.gif')]  # 정지 할 때의 이미지
        self.image_walk = [load_image('mayreel/walk/walk_00.gif'),
                           load_image('mayreel/walk/walk_01.gif'),
                           load_image('mayreel/walk/walk_02.gif'),
                           load_image('mayreel/walk/walk_03.gif'),
                           load_image('mayreel/walk/walk_04.gif'),
                           load_image('mayreel/walk/walk_05.gif'),
                           load_image('mayreel/walk/walk_06.gif'),
                           load_image('mayreel/walk/walk_07.gif'),
                           load_image('mayreel/walk/walk_08.gif'),
                           load_image('mayreel/walk/walk_09.gif'),
                           load_image('mayreel/walk/walk_10.gif')]  # 달릴 때의 이미지
        self.image_jump_up = [load_image('mayreel/jump_up/jump_00.gif'),
                              load_image('mayreel/jump_up/jump_01.gif'),
                              load_image('mayreel/jump_up/jump_02.gif'),
                              load_image('mayreel/jump_up/jump_03.gif'),
                              load_image('mayreel/jump_up/jump_04.gif'),
                              load_image('mayreel/jump_up/jump_05.gif'),
                              load_image('mayreel/jump_up/jump_06.gif'),
                              load_image('mayreel/jump_up/jump_07.gif'),
                              load_image('mayreel/jump_up/jump_08.gif'),
                              load_image('mayreel/jump_up/jump_09.gif')]  # 위로 튀어오를 때 이미지
        self.image_jump_down = [load_image('mayreel/jump_down/jump_10.gif'),
                                load_image('mayreel/jump_down/jump_11.gif'),
                                load_image('mayreel/jump_down/jump_12.gif')]  # 아래로 떨어질 때 이미지
        self.image_slide = load_image('mayreel/bari_mayreel_slide.png')  # 슬라이딩 할 때 이미지

        self.speed = 0  # 좌우 이동 속도
        self.direction = 'r'  # r= 오른쪽, h= 왼쪽
        self.gravity = 0  # 떨어 질 때의 속도
        self.jump_power = 0  # 점프 하는 힘
        self.jump_power_max = 5  # 점프 하는 힘 한계치
        self.jump_count = 1  # 남은 점프 횟수

    def update(self):
        global press_left
        global press_right

        if (press_left, press_right) == (True, False):
            if 0 >= self.speed > -0.8:
                self.speed -= 0.02
            elif 0.8 >= self.speed > 0:
                self.speed -= 0.005
            elif self.speed <= -0.8:
                self.speed = -0.8
        elif (press_left, press_right) == (False, True):
            if 0 <= self.speed < 0.8:
                self.speed += 0.02
            elif -0.8 <= self.speed < 0:
                self.speed += 0.005
            elif self.speed >= 0.8:
                self.speed = 0.8
        else:
            if -0.1 <= self.speed <= 0.1:
                self.speed = 0
            elif self.speed > 0.1:
                self.speed -= 0.002
            elif self.speed < -0.1:
                self.speed += 0.002

        # ----------------------------------------------------------------------- # 캐릭터 이동
        if self.gravity < 2:
            self.gravity += 0.05
        if self.jump_power > 0:
            if 1 >= (self.jump_power / self.jump_power_max) > 0.66:
                self.jump_power -= 0.015
            elif 0.66 >= (self.jump_power / self.jump_power_max) > 0.33:
                self.jump_power -= 0.025
            elif 0.33 >= (self.jump_power / self.jump_power_max) > 0:
                self.jump_power -= 0.035
        elif self.jump_power <= 0:  # 점프력이 0이 되면 더 안내려감
            self.jump_power = 0
        # ----------------------------------------------------------------------- # 캐릭터가 땅에 닿으면
        if self.y <= 0:
            self.y = 0
            self.gravity = 0
            if self.jump_power <= self.jump_power_max - 0.5:
                self.jump_count = 1
        # ----------------------------------------------------------------------- # 캐릭터가 중력에 따라 위아래로 이동
        self.frame_sec += 1  # 프레임 증가
        if self.frame_sec >= self.frame_sec_all:  # 프레임 초 n당 프레임 1 지나감
            if self.frame < self.frame_ani - 1:  # 애니메이션 시트 총 프레임 frame_ani
                self.frame += 1
            elif self.frame == self.frame_ani - 1:
                if self.frame_loop != 'loop':
                    pass
                elif self.frame_loop == 'loop':
                    self.frame = 0
            self.frame_sec = 0
        # ----------------------------------------------------------------------- # 캐릭터 행동에 따라 상태 변환
        if self.status == 'slide':
            pass
        elif (self.jump_power - self.gravity) != 0:  # 캐릭터가 위아래로 움직이는 상태면 점프상태
            if self.jump_power > self.gravity:
                self.status = 'jump_up'
            elif self.jump_power <= self.gravity:
                self.status = 'jump_down'
        elif self.speed != 0:
            self.status = 'walk'

        elif self.speed == 0:  # 속도가 0이면 멈춘 상태로 바꾼다.
            self.status = 'idle'
        # ----------------------------------------------------------------------- # 이동 방향에 따라 스프라이트 방향 변경
        if self.speed > 0:
            self.direction = 'r'  # 오른쪽으로 가면 이미지가 오른쪽방향
        elif self.speed < 0:
            self.direction = 'h'  # 왼쪽으로 가면 이미지가 왼쪽방향
        # ----------------------------------------------------------------------- # 캐릭터 상태에 따라 애니메이션 프레임 변경
        if self.status == 'idle':  # 멈춘 상태에서는 총 프레임 14
            self.frame_ani = 14
            self.frame_sec_all = 20
            self.frame_loop = 'loop'
        elif self.status == 'walk':
            self.frame_ani = 11
            self.frame_sec_all = 20
            self.frame_loop = 'loop'
        elif self.status == 'slide':
            self.frame_ani = 5
            self.frame_sec_all = 20
            self.frame_loop = 'no'
        elif self.status == 'jump_up':
            self.frame_ani = 10
            self.frame_sec_all = 10
            self.frame_loop = 'no'
        elif self.status == 'jump_down':
            self.frame_ani = 3
            self.frame_sec_all = 50
            self.frame_loop = 'no'
        # -----------------------------------------------------------------------
        if self.status == self.status_save:  # 현재 상태가 바뀌지 않았다면
            pass
        elif self.status != self.status_save:  # 현재 상태가 바뀌었다면
            self.status_save = self.status
            self.frame = 0
            self.frame_sec = 0

        if self.run:
            self.run_speed = 1.5
            if self.status == 'walk':
                self.frame_sec_all = 13
        else:
            self.run_speed = 1

        # ----------------------------------------------------------------------- # 플레이어 이동
        self.x += self.speed * self.run_speed  # 좌우 이동 속도 만큼 초당 움직임
        self.y = self.y + self.jump_power - self.gravity  # 점프 힘 - 떨어지는 힘 만큼 위 아래로 이동

    def draw(self):
        # rad = 각도(라디안 단위) h=좌우 대칭, v=상하 대칭
        if self.status == 'jump_up':

            self.image_jump_up[self.frame].clip_composite_draw(0, 0, self.image_jump_up[self.frame].w_value(),
                                                               self.image_jump_up[self.frame].h_value(), 0,
                                                               self.direction,
                                                               self.x,
                                                               self.y + self.image_jump_up[
                                                                   self.frame].h_value() // 8,
                                                               self.image_jump_up[self.frame].w_value() // 4,
                                                               self.image_jump_up[self.frame].h_value() // 4)
        elif self.status == 'jump_down':
            self.image_jump_down[self.frame].clip_composite_draw(0, 0, self.image_jump_down[self.frame].w_value(),
                                                                 self.image_jump_down[self.frame].h_value(), 0,
                                                                 self.direction,
                                                                 self.x,
                                                                 self.y + self.image_jump_down[
                                                                     self.frame].h_value() // 8,
                                                                 self.image_jump_down[self.frame].w_value() // 4,
                                                                 self.image_jump_down[self.frame].h_value() // 4)

        elif self.status == 'idle':
            self.image_idle[self.frame].clip_composite_draw(0, 0, self.image_idle[self.frame].w_value(),
                                                            self.image_idle[self.frame].h_value(), 0, self.direction,
                                                            self.x,
                                                            self.y + self.image_idle[self.frame].h_value() // 8,
                                                            self.image_idle[self.frame].w_value() // 4,
                                                            self.image_idle[self.frame].h_value() // 4)

        elif self.status == 'walk':
            self.image_walk[self.frame].clip_composite_draw(0, 0, self.image_walk[self.frame].w_value(),
                                                            self.image_walk[self.frame].h_value(), 0, self.direction,
                                                            self.x,
                                                            self.y + self.image_walk[self.frame].h_value() // 8,
                                                            self.image_walk[self.frame].w_value() // 4,
                                                            self.image_walk[self.frame].h_value() // 4)
        elif self.status == 'slide':
            self.image_slide.clip_composite_draw(self.frame * 32, 0, 32, 32, 0, self.direction, self.x,
                                                 self.y, 272, 272)


def enter():
    global player, block, sky, font
    sky = Sky()
    player = Player()
    block = Block()

    pass


def exit():
    global player, block, font
    del player
    del block

    global press_left  # 키 초기화
    global press_right
    press_left, press_right = False, False

    pass


def pause():
    pass


def resume():
    pass


def handle_events():
    events = get_events()
    global press_left
    global press_right

    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_SPACE):
            game_framework.change_state(title_state)
        # 좌우 키 누르면 좌우로 이동
        if (event.type, event.key, press_left) == (SDL_KEYDOWN, SDLK_LEFT, False):
            press_left = True  # 왼쪽 키를 누른 상태가 됨 # 플레이어가 이동 상태가 됨
        elif (event.type, event.key, press_left) == (SDL_KEYUP, SDLK_LEFT, True):
            press_left = False  # 플레이어가 정지 상태가 됨
        elif (event.type, event.key, press_right) == (SDL_KEYDOWN, SDLK_RIGHT, False):
            press_right = True  # 플레이어가 이동 상태가 됨
        elif (event.type, event.key, press_right) == (SDL_KEYUP, SDLK_RIGHT, True):
            press_right = False  # 플레이어가 정지 상태가 됨

        if (event.type, event.key) == (SDL_KEYDOWN, SDLK_z):  # 점프
            if player.jump_count > 0:
                player.jump_count -= 1
                player.gravity = 0
                player.jump_power = player.jump_power_max

        if (event.type, event.key) == (SDL_KEYDOWN, SDLK_x):  # 달리기
            player.run = True
        elif (event.type, event.key) == (SDL_KEYUP, SDLK_x):
            player.run = False

        if (event.type, event.key) == (SDL_KEYDOWN, SDLK_DOWN):  # 슬라이딩
            player.status = 'slide'
        elif (event.type, event.key) == (SDL_KEYUP, SDLK_DOWN):
            player.status = 'idle'

    pass


def update():
    player.update()
    pass


def draw():
    clear_canvas()
    sky.draw()
    block.draw()
    player.draw()
    update_canvas()
    pass
