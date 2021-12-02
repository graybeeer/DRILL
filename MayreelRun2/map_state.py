from pico2d import *

import game_framework
import game_world
import main_state
import server
from block import Block
from sky import Sky

name = "MapState"

code = 0  # 블럭 코드


class UI:
    def __init__(self):
        self.font = load_font('ENCR10B.TTF', 16)

    def draw(self):
        self.font.draw(800, 600, '(%d,%d)' % (server.cx, server.cy), (255, 255, 0))


def enter():
    server.ui = UI()
    server.sky = Sky()
    server.cx = 0
    server.cy = 0
    # game_world.add_object(server.sky, 1)
    game_world.add_objects(server.block, 1)
    pass


def exit():
    game_world.clear()


def pause():
    pass


def resume():
    pass


def handle_events():
    global code
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
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_2):
            code = 1
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_3):
            code = 2

        if (event.type, event.key) == (SDL_KEYDOWN, SDLK_LEFT):  # 카메라 이동
            server.cx += 100
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_RIGHT):
            server.cx -= 100
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_UP):  # 카메라 이동
            server.cy -= 100
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_DOWN):
            server.cy += 100
        if (event.type, event.button) == (SDL_MOUSEBUTTONDOWN, SDL_BUTTON_LMASK): #마우스 좌클릭 블럭 추가
            for i in range(len(server.block)):
                if server.block[i].col_left < event.x - server.cx < server.block[i].col_right:
                    if server.block[i].col_bottom < get_canvas_height() - event.y - server.cy < server.block[i].col_top:
                        game_world.remove_object(server.block[i])
                        del (server.block[i])
                        break
            server.block += [
                Block(100 * ((event.x - server.cx) // 100) + 50,
                      100 * ((get_canvas_height() - event.y - server.cy) // 100) + 50, code)]
            game_world.add_object(server.block[len(server.block) - 1], 2)

        elif (event.type, event.button) == (SDL_MOUSEBUTTONDOWN, SDL_BUTTON_RMASK):  # 마우스 위아래 버튼 아래

            if server.block is not None:
                for i in range(len(server.block)):
                    if server.block[i].col_left < event.x - server.cx < server.block[i].col_right:
                        if server.block[i].col_bottom < get_canvas_height() - event.y - server.cy < server.block[
                            i].col_top:
                            game_world.remove_object(server.block[i])
                            del (server.block[i])
                            break


def update():
    for game_object in game_world.all_objects():
        game_object.update()


def draw():
    clear_canvas()
    for game_object in game_world.all_objects():
        if -500 < game_object.x + server.cx < 2500 and -500 < game_object.y + server.cy < 1500:
            game_object.draw()
    server.ui.draw()

    update_canvas()
