from pico2d import *

import game_framework
import game_world
import main_state
import start_state
import server
from background import Background
from block import Block
from ddat import Ddat

name = "MapState"

code = 0  # 코드 숫자
code_class = 'block'  # 코드 종류


class UI:
    def __init__(self):
        self.font = load_font('a시월구일2.ttf', 20)
        self.image_ui = load_image('ui/whiteboard.png')

    def draw(self):

        for i in range(server.map_area_x):
            for j in range(server.map_area_y):
                self.font.draw(50 + 1000 * i + server.cx, 950 + 1000 * j + server.cy, '(%d,%d)' % (i, j), (0, 0, 0))
        for i in range(5):
            self.image_ui.clip_draw(0, 0, self.image_ui.w, self.image_ui.h, 300 * i + 150, 825, 250, 100)
            draw_rectangle(300 * i + 25, 775, 300 * i + 150, 875)
            draw_rectangle(300 * i + 150, 775, 300 * i + 275, 875)
            self.font.draw(300 * i + 25, 825, "세이브 " + "%d " % (i + 1) + "저장", (0, 0, 0))
            self.font.draw(300 * i + 150, 825, "세이브 " + "%d " % (i + 1) + "로드", (0, 0, 0))


def enter():
    server.cx = 0
    server.cy = 0
    server.player = None
    game_world.add_objects(server.background, 1)
    game_world.add_objects(server.block, 2)
    game_world.add_objects(server.monster, 3)
    server.ui = UI()
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
            game_framework.change_state(start_state)
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
            code = 3
            code_class = 'block'
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_5):
            code = 4
            code_class = 'block'
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_6):
            code = 0
            code_class = 'monster'
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_F1):
            code = 0
            code_class = 'background'
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_F2):
            code = 1
            code_class = 'background'
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_F3):
            code = 2
            code_class = 'background'
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_F4):
            code = 3
            code_class = 'background'
        """if (event.type, event.key) == (SDL_KEYDOWN, SDLK_q):
            game_world.save()
        if (event.type, event.key) == (SDL_KEYDOWN, SDLK_w):
            load_saved_world()"""
        if (event.type, event.key) == (SDL_KEYDOWN, SDLK_LEFT):  # 카메라 이동
            server.cx += 200
            server.cx = clamp(-(server.map_area_size_x * server.map_area_x - get_canvas_width()), server.cx, 0)
            # 카메라 범위 제한
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_RIGHT):
            server.cx -= 200
            server.cx = clamp(-(server.map_area_size_x * server.map_area_x - get_canvas_width()), server.cx, 0)
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_UP):  # 카메라 이동
            server.cy -= 200
            server.cy = clamp(-(server.map_area_size_y * server.map_area_y - get_canvas_height()), server.cy, 0)
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_DOWN):
            server.cy += 200
            server.cy = clamp(-(server.map_area_size_y * server.map_area_y - get_canvas_height()), server.cy, 0)
        left_click = 0
        if (event.type, event.button) == (SDL_MOUSEBUTTONDOWN, SDL_BUTTON_LMASK):  # 마우스 좌클릭 세이브 로드
            for i in range(5):
                if 300 * i + 25 < event.x < 300 * i + 150:
                    if 775 < get_canvas_height() - event.y < 875:
                        game_world.save(i)
                        left_click = 1
                        break
                elif 300 * i + 150 < event.x < 300 * i + 275:
                    if 775 < get_canvas_height() - event.y < 875:
                        load_saved_world(i)
                        left_click = 1
                        break
        if (event.type, event.button) == (SDL_MOUSEBUTTONDOWN, SDL_BUTTON_LMASK) and left_click == 0:  # 마우스 좌클릭 블럭 추가
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
            """for i in range(len(server.background)):  # 배경 블럭 삭제
                if server.background[i].x - 50 < event.x - server.cx < server.background[i].x + 50:
                    if server.background[i].y <= get_canvas_height() - event.y - server.cy < server.background[
                        i].y + 100:
                        game_world.remove_object(server.background[i])
                        del (server.background[i])
                        break"""
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
                    game_world.add_object(server.monster[len(server.monster) - 1], 3)
            elif code_class == 'background':
                server.background += [
                    Background(100 * ((event.x - server.cx) // 100) + 50,
                               100 * ((get_canvas_height() - event.y - server.cy) // 100), code)]
                game_world.add_object(server.background[len(server.background) - 1], 1)


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
            for i in range(len(server.background)):  # 배경 블럭 삭제
                if server.background[i].x - 50 < event.x - server.cx < server.background[i].x + 50:
                    if server.background[i].y <= get_canvas_height() - event.y - server.cy < server.background[
                        i].y + 100:
                        game_world.remove_object(server.background[i])
                        del (server.background[i])
                        break


def update():
    for game_object in game_world.all_objects():
        game_object.update()


def draw():
    clear_canvas()
    for game_object in game_world.all_objects():
        game_object.draw()
    for i in range(server.map_area_x):
        for j in range(server.map_area_y):
            draw_rectangle(server.map_area_size_x * i + server.cx, server.map_area_size_y * i + server.cy,
                           server.map_area_size_x * (j + 1) + server.cx,
                           server.map_area_size_y * (j + 1) + server.cy)

    server.ui.draw()
    update_canvas()


def load_saved_world(i):
    game_world.load(i)
    server.block = []
    server.monster = []
    server.background = []
    for o in game_world.all_objects():
        if isinstance(o, Block):
            server.block.append(o)
        elif isinstance(o, Ddat):
            server.monster.append(o)
        elif isinstance(o, Background):
            server.background.append(o)
    print('load')
