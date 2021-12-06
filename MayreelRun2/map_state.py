from pico2d import *

import game_framework
import game_world
import main_state
import server
from block import Block
from ddat import Ddat

name = "MapState"

code = 0  # 코드 숫자
code_class = 'block'  # 코드 종류


class UI:
    def __init__(self):
        self.font = load_font('a시월구일2.ttf', 20)

    def draw(self):
        for i in range(server.map_area_x):
            for j in range(server.map_area_y):
                self.font.draw(50 + 1000 * i + server.cx, 950 + 1000 * j + server.cy, '(%d,%d)' % (i, j), (0, 0, 0))


def enter():
    server.ui = UI()
    server.cx = 0
    server.cy = 0
    server.player = None
    game_world.add_objects(server.block, 1)
    game_world.add_objects(server.block_sleep, 1)
    game_world.add_objects(server.monster, 2)
    pass


def exit():
    game_world.clear()


def pause():
    pass


def resume():
    pass


def handle_events():
    global code, code_class
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_SPACE:
            game_framework.change_state(main_state)
        if (event.type, event.key) == (SDL_KEYDOWN, SDLK_1):
            code = 0
            code_class = 'block'
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_2):
            code = 1
            code_class = 'block'
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_3):
            code = 2
            code_class = 'block'
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_4):
            code = 0
            code_class = 'monster'

        if (event.type, event.key) == (SDL_KEYDOWN, SDLK_LEFT):  # 카메라 이동
            server.cx += 100
            server.cx = clamp(-5000, server.cx, 0)  # 카메라 범위 제한
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_RIGHT):
            server.cx -= 100
            server.cx = clamp(-5000, server.cx, 0)
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_UP):  # 카메라 이동
            server.cy -= 100
            server.cy = clamp(-5000, server.cy, 0)
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_DOWN):
            server.cy += 100
            server.cy = clamp(-5000, server.cy, 0)
        if (event.type, event.button) == (SDL_MOUSEBUTTONDOWN, SDL_BUTTON_LMASK):  # 마우스 좌클릭 블럭 추가
            for i in range(len(server.block)):
                if server.block[i].col_left < event.x - server.cx < server.block[i].col_right:
                    if server.block[i].col_bottom < get_canvas_height() - event.y - server.cy < server.block[
                        i].col_top:
                        game_world.remove_object(server.block[i])
                        del (server.block[i])
                        break
            for i in range(len(server.monster)):
                if server.monster[i].x - 50 < event.x - server.cx < server.monster[i].x + 50:
                    if server.monster[i].col_bottom < get_canvas_height() - event.y - server.cy < server.monster[
                        i].col_bottom + 100:
                        game_world.remove_object(server.monster[i])
                        del (server.monster[i])
                        break
            if code_class == 'block':
                server.block += [
                    Block(100 * ((event.x - server.cx) // 100) + 50,
                          100 * ((get_canvas_height() - event.y - server.cy) // 100) + 50, code)]
                game_world.add_object(server.block[len(server.block) - 1], 2)

            elif code_class == 'monster':
                if code == 0:
                    server.monster += [
                        Ddat(100 * ((event.x - server.cx) // 100) + 50,
                             100 * ((get_canvas_height() - event.y - server.cy) // 100) + 80)]
                    game_world.add_object(server.monster[len(server.monster) - 1], 2)


        elif (event.type, event.button) == (SDL_MOUSEBUTTONDOWN, SDL_BUTTON_RMASK):  # 마우스 위아래 버튼 아래
            if server.block is not None:
                for i in range(len(server.block)):
                    if server.block[i].col_left < event.x - server.cx < server.block[i].col_right:
                        if server.block[i].col_bottom < get_canvas_height() - event.y - server.cy < server.block[
                            i].col_top:
                            game_world.remove_object(server.block[i])
                            del (server.block[i])
                            break
            if server.monster is not None:
                for i in range(len(server.monster)):
                    if server.monster[i].x - 50 < event.x - server.cx < server.monster[i].x + 50:
                        if server.monster[i].col_bottom < get_canvas_height() - event.y - server.cy < server.monster[
                            i].col_bottom + 100:
                            game_world.remove_object(server.monster[i])
                            del (server.monster[i])
                            break


def update():
    for game_object in game_world.all_objects():
        game_object.update()


def draw():
    clear_canvas()
    for game_object in game_world.all_objects():
        game_object.draw()
    for i in range(10):
        for j in range(10):
            draw_rectangle(1000 * i + server.cx, 1000 * i + server.cy, 1000 * (j + 1) + server.cx,
                           1000 * (j + 1) + server.cy)
    server.ui.draw()

    update_canvas()

def save():
    pass
