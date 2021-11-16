import json
import os
import random

import game_framework
import game_world
import title_state
from block import Block
from pico2d import *
from player import Player, press_left, press_right

name = "MainState"

sky = None
player = None
block = None
blocks = None
font = None


# 코딩 정리
# 1. 콜라이더 박스 순서 [왼쪽, 아래쪽, 오른쪽, 위쪽]
# 2. 마우스 입력시 y값은 다른것과는 반대로 화면 맨 위가 0이다.
# get_canvas_height() - player.col_rect[1] >= event.y >= get_canvas_height() - player.col_rect[3]:
#
#
#

def collide(a, b):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()
    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False
    return True


class Sky:
    def __init__(self):
        self.image = load_image('background_sky.png')

    def draw(self):
        self.image.clip_draw(0, 0, 32, 64, 750, 450, 1500, 900)


def enter():
    global sky
    sky = Sky()

    global player
    player = Player()
    game_world.add_object(player, 1)

    pass


def exit():
    global player, block, font
    del player
    del block

    global press_left  # 키 초기화
    global press_right
    press_left, press_right = False, False
    game_world.clear()

    pass


def pause():
    pass


def resume():
    pass


def handle_events():
    global block
    events = get_events()
    for event in events:

        player.handle_event(event)
        if (event.type, event.button) == (SDL_MOUSEBUTTONDOWN, SDL_BUTTON_LMASK):
            if block is None:
                block = [(Block(event.x, get_canvas_height() - event.y))]
                game_world.add_object(block[0], 2)
            else:
                block += [(Block(event.x, get_canvas_height() - event.y))]
                game_world.add_object(block[len(block) - 1], 2)

        if event.type == SDL_QUIT:
            game_framework.quit()
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_SPACE):
            game_framework.change_state(title_state)


def update():
    for game_object in game_world.all_objects():
        game_object.update()
    if block is not None:
        for i in range(len(block)):
            if collide(player, block[i]):
                if player.col_rect[1] >= block[i].col_rect[3] - 10:  # 블럭 위
                    player.y = block[i].col_rect[3]
                    player.jump_power = 0
                    player.gravity = 0
                    if player.jump_power <= player.jump_power_max - 0.5:
                        player.jump_count = 1
                elif player.col_rect[2] <= block[i].col_rect[0] + 10:  # 블럭 왼쪽
                    player.x = block[i].col_rect[0] - player.col_xsize
                elif player.col_rect[0] >= block[i].col_rect[2] - 10:  # 블럭 오른쪽
                    player.x = block[i].col_rect[2] + player.col_xsize
                elif player.col_rect[3] <= block[i].col_rect[1] + 10:  # 블럭 아래쪽
                    if player.jump_power - player.gravity >= 0:
                        player.jump_power = 0
                        player.gravity = 0
                        player.y = block[i].col_rect[1] - player.col_ysize
    pass


def draw():
    clear_canvas()
    sky.draw()
    for game_object in game_world.all_objects():
        game_object.draw()
    update_canvas()
