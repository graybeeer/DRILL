from pico2d import *

import game_framework
import title_state

name = "MainState"

player = None
grass = None
font = None
press_left = False  # 왼쪽키를 누른 상태인지 아닌지
press_right = False  # 오른쪽키를 누른 상태인지 아닌지


class Grass:
    def __init__(self):
        self.image = load_image('grass.png')

    def draw(self):
        self.image.draw(400, 30)


class Player:
    def __init__(self):
        self.status = 'stop'  # stop=멈춘상태 run= 달리는 상태 jump=공중에 있는 상태 slide=슬라이딩 상태
        self.status_save = 'stop'  # 바로 전 프레임의 플레이어 상태
        self.x, self.y = 0, 300  # 캐릭터 위치
        self.frame = 0  # 캐릭터 프레임
        self.frame_sec = 0  # 캐릭터 프레임 시간이 일정 지날때마다 캐릭터 프레임 증가
        self.frame_ani = 0  # 캐릭터 애니메이션의 총 프레임

        self.image_idle = load_image('bari_mayreel_idle.png')  # 정지 할 때의 이미지
        self.image_run = load_image('mayreel_run_Sheet.png')  # 달릴 때의 이미지
        self.image_jump_up = load_image('mayreel_jump_1.png')  # 위로 튀어오를 때 이미지
        self.image_jump_down = load_image('mayreel_jump_2.png')  # 아래로 떨어질 때 이미지
        self.image_jump_slide = load_image('mayreel_slide-Sheet.png')  # 슬라이딩 할 때 이미지

        self.dir = 0  # 좌우 이동 속도
        self.direction = 'r'  # r= 오른쪽, h= 왼쪽
        self.gravity = 0  # 떨어 질 때의 속도
        self.jump_power = 0  # 점프 하는 힘
        self.jump_count = 2  # 남은 점프 횟수

    def update(self):

        self.x += self.dir  # 좌우 이동 속도 만큼 초당 움직임
        if self.gravity < 2:
            self.gravity += 0.05
        if self.jump_power > 0:
            self.jump_power -= 0.025
        elif self.jump_power <= 0:  # 점프력이 0이 되면 더 안내려감
            self.jump_power = 0

        self.y = self.y + self.jump_power - self.gravity  # 점프 힘 - 떨어지는 힘 만큼 위 아래로 이동
        if self.y < 80:
            self.y = 80
            self.gravity = 0
            self.jump_count = 2

        self.frame_sec += 1  # 프레임 증가
        if self.frame_sec >= 20:  # 프레임 초 n당 프레임 1 지나감
            if self.frame < 4:  # 슬라이딩 시트 총 프레임 5, 5번째 프레임에서 멈춤
                self.frame += 1
            self.frame_sec = 0

        if self.jump_power > 0:  # 캐릭터 행동에 따라 상태 변환
            self.status = 'jump'
        elif self.dir != 0:
            self.status = 'run'

            if self.dir > 0:
                self.direction = 'r'
            elif self.dir < 0:
                self.direction = 'h'

        elif self.dir == 0:
            self.status = 'stop'

        if self.status == 'stop':
            self.frame_ani = 14
        elif self.status == 'run':
            self.frame_ani = 10
        elif self.status == 'slide':
            self.frame_ani = 5

        if self.status == self.status_save:  # 현재 상태가 바뀌지 않았다면
            pass
        if self.status != self.status_save:  # 현재 상태가 바뀌었다면
            self.status_save = self.status
            self.frame = 0
            self.frame_sec = 0

    def draw(self):
        # rad = 각도(라디안 단위) h=좌우 대칭, v=상하 대칭
        if self.status == 'jump':
            if self.jump_power > self.gravity:
                self.image_jump_up.clip_composite_draw(0, 0, 32, 32, 0, self.direction, self.x, self.y, 128, 128)
            elif self.jump_power <= self.gravity:
                self.image_jump_down.clip_composite_draw(0, 0, 32, 32, 0, self.direction, self.x, self.y, 128, 128)

        elif self.status == 'stop':
            self.image_idle.clip_composite_draw(self.frame * 272, 0, 272, 272, 0, self.direction, self.x, self.y)

        elif self.status == 'run':
            self.image_run.clip_composite_draw(self.frame * 32, 0, 32, 32, 0, self.direction, self.x, self.y, 128,
                                               128)
        elif self.status == 'slide':
            self.image_jump_slide.clip_composite_draw(self.frame * 32, 0, 32, 32, 0, self.direction, self.x,
                                                      self.y,
                                                      128, 128)


def enter():
    global player, grass
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
            player.status = 'stop'

    pass


def update():
    player.update()
    pass


def draw():
    clear_canvas()
    grass.draw()
    player.draw()
    update_canvas()
    pass
