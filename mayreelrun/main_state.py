from pico2d import *

import game_framework
import title_state

name = "MainState"

sky = None
player = None
grass = None

press_left = False  # 왼쪽키를 누른 상태인지 아닌지
press_right = False  # 오른쪽키를 누른 상태인지 아닌지


class Sky:
    def __init__(self):
        self.image = load_image('background_sky.png')

    def draw(self):
        self.image.clip_draw(0, 0, 32, 64, 400, 300, 800, 600)


class Grass:
    def __init__(self):
        self.image = load_image('grass.png')

    def draw(self):
        self.image.draw(400, 30)


class Player:
    def __init__(self):

        self.status = 'idle'  # idle=멈춘상태 walk= 달리는 상태 jump=공중에 있는 상태 slide=슬라이딩 상태
        self.status_save = 'idle'  # 바로 전 프레임의 플레이어 상태
        self.x, self.y = 0, 300  # 캐릭터 위치
        self.frame = 0  # 캐릭터 프레임
        self.frame_sec = 0  # 캐릭터 프레임 시간이 일정 지날때마다 캐릭터 1 프레임 증가
        self.frame_sec_all = 0  # 캐릭터 1프레임 당 시간
        self.frame_ani = 0  # 캐릭터 애니메이션의 총 프레임
        self.frame_loop = 'loop'  # loop면 애니메이션 반복
        self.w = 1088  # 플레이어 메이릴 이미지의 크기
        self.h = 1088
        self.col = [(self.y - 68), (self.x - 5), (self.y - 136), (self.x + 50)]  # top,left,bottom,right

        # 배열을 이용해 여러개의 이미지를 하나의 변수에 넣을 수 있다.
        self.image_idle = [load_image('mayreel/bari_mayreel_idle.png')]  # 정지 할 때의 이미지
        self.image_walk = load_image('mayreel/bari_mayreel_walk.png')  # 달릴 때의 이미지
        self.image_jump_up = load_image('mayreel/bari_mayreel_jump_1.png')  # 위로 튀어오를 때 이미지
        self.image_jump_down = load_image('mayreel/bari_mayreel_jump_2.png')  # 아래로 떨어질 때 이미지
        self.image_slide = load_image('mayreel/bari_mayreel_slide.png')  # 슬라이딩 할 때 이미지

        self.dir = 0  # 좌우 이동 속도
        self.direction = 'r'  # r= 오른쪽, h= 왼쪽
        self.gravity = 0  # 떨어 질 때의 속도
        self.jump_power = 0  # 점프 하는 힘
        self.jump_count = 2  # 남은 점프 횟수

    def update(self):

        self.x += self.dir * 0.5  # 좌우 이동 속도 만큼 초당 움직임
        if self.gravity < 2:
            self.gravity += 0.05
        if self.jump_power > 0:
            self.jump_power -= 0.025
        elif self.jump_power <= 0:  # 점프력이 0이 되면 더 안내려감
            self.jump_power = 0
        # ----------------------------------------------------------------------- # 캐릭터가 땅에 닿으면
        if self.col[2] < 0:
            self.col[2] = 0
            self.gravity = 0
            self.jump_count = 2
        # ----------------------------------------------------------------------- # 캐릭터가 중력에 따라 위아래로 이동
        self.y = self.y + self.jump_power - self.gravity  # 점프 힘 - 떨어지는 힘 만큼 위 아래로 이동

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
            self.status = 'jump'
        elif self.dir != 0:
            self.status = 'walk'
            if self.dir > 0:
                self.direction = 'r'  # 오른쪽으로 가면 이미지가 오른쪽방향
            elif self.dir < 0:
                self.direction = 'h'  # 왼쪽으로 가면 이미지가 왼쪽방향
        elif self.dir == 0:  # 속도가 0이면 멈춘 상태로 바꾼다.
            self.status = 'idle'
        # ----------------------------------------------------------------------- # 캐릭터 상태에 따라 애니메이션 프레임 변경
        if self.status == 'idle':  # 멈춘 상태에서는 총 프레임 14
            self.frame_ani = 14
            self.frame_sec_all = 20
            self.frame_loop = 'loop'
        elif self.status == 'walk':
            self.frame_ani = 10
            self.frame_sec_all = 20
            self.frame_loop = 'loop'
        elif self.status == 'slide':
            self.frame_ani = 5
            self.frame_sec_all = 20
            self.frame_loop = 'no'
        elif self.status == 'jump':
            if self.jump_power > self.gravity:
                self.frame_ani = 11
                self.frame_sec_all = 10
                self.frame_loop = 'no'
            elif self.jump_power <= self.gravity:
                self.frame_ani = 2
                self.frame_sec_all = 10
                self.frame_loop = 'no'
        # -----------------------------------------------------------------------
        if self.status == self.status_save:  # 현재 상태가 바뀌지 않았다면
            pass
        elif self.status != self.status_save:  # 현재 상태가 바뀌었다면
            self.status_save = self.status
            self.frame = 0
            self.frame_sec = 0
        # ----------------------------------------------------------------------- # 플레이어 콜라이더 이동
        self.col = [(self.y - 68), (self.x - 5), (self.y - 136), (self.x + 50)]  # top,left,bottom,right

    def draw(self):
        # rad = 각도(라디안 단위) h=좌우 대칭, v=상하 대칭
        if self.status == 'jump':
            if self.jump_power > self.gravity:
                self.image_jump_up.clip_composite_draw(self.frame * 1088, 0, self.w, self.h, 0, self.direction, self.x,
                                                       self.y, 272, 272)
            elif self.jump_power <= self.gravity:
                self.image_jump_down.clip_composite_draw(0, 0, self.w, self.h, 0, self.direction, self.x,
                                                         self.y, 272, 272)

        elif self.status == 'idle':
            self.image_idle[0].clip_composite_draw(self.frame * 1088, 0, self.w, self.h, 0, self.direction, self.x,
                                                   self.y,
                                                   self.w / 4, self.image_idle[0].h_value() / 4)

        elif self.status == 'walk':
            self.image_walk.clip_composite_draw(self.frame * 1088, 0, self.w, self.h, 0, self.direction, self.x, self.y,
                                                self.w / 4, self.h / 4)
        elif self.status == 'slide':
            self.image_slide.clip_composite_draw(self.frame * 32, 0, 32, 32, 0, self.direction, self.x,
                                                 self.y, 272, 272)


def enter():
    global player, grass, sky
    sky = Sky()
    player = Player()
    grass = Grass()

    pass


def exit():
    global player, grass
    del player
    del grass
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
            player.dir -= 1  # 플레이어가 이동 상태가 됨
            player.direction = 'h'  # 플레이어가 왼쪽 방향이 됨
            press_left = True  # 왼쪽 키를 누른 상태가 됨
        elif (event.type, event.key, press_left) == (SDL_KEYUP, SDLK_LEFT, True):
            player.dir += 1  # 플레이어가 정지 상태가 됨
            press_left = False
        elif (event.type, event.key, press_right) == (SDL_KEYDOWN, SDLK_RIGHT, False):
            player.dir += 1  # 플레이어가 이동 상태가 됨
            player.direction = 'r'
            press_right = True
        elif (event.type, event.key, press_right) == (SDL_KEYUP, SDLK_RIGHT, True):
            player.dir -= 1  # 플레이어가 정지 상태가 됨
            press_right = False

        if (event.type, event.key) == (SDL_KEYDOWN, SDLK_z):  # 점프
            if player.jump_count > 0:
                player.jump_count -= 1
                player.gravity = 0
                player.jump_power = 5

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
    grass.draw()
    player.draw()
    update_canvas()
    pass
