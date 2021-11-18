from pico2d import *

import game_framework
import game_world
import main_state
from block import Block

name = "MapState"
player = None
block = []
ui = None
camera_x = 0
camera_y = 0


class UI:
    def __init__(self):
        self.font = load_font('ENCR10B.TTF', 16)

    def draw(self):
        self.font.draw(800, 600, '(%3.2f)' % len(block), (255, 255, 0))


def enter():
    global block
    global ui
    ui = UI()
    for i in range(len(block)):
        game_world.add_object(block[i], 2)
    pass


def exit():
    game_world.clear()


def pause():
    pass


def resume():
    pass


def handle_events():
    global block, camera_x, camera_y
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_SPACE:
            game_framework.change_state(main_state)

        if (event.type, event.button) == (SDL_KEYDOWN, SDLK_LEFT):
            camera_x -= 100
        elif (event.type, event.button) == (SDL_KEYDOWN, SDLK_RIGHT):
            camera_x += 100
        if (event.type, event.button) == (SDL_MOUSEBUTTONDOWN, SDL_BUTTON_LMASK):
            if block is None:
                block = [(Block(100 * (event.x // 100) + 50, 100 * ((get_canvas_height() - event.y) // 100) + 50))]
                game_world.add_object(block[0], 2)
            else:
                block += [(Block(100 * (event.x // 100) + 50, 100 * ((get_canvas_height() - event.y) // 100) + 50))]
                game_world.add_object(block[len(block) - 1], 2)

        elif (event.type, event.button) == (SDL_MOUSEBUTTONDOWN, SDL_BUTTON_RMASK):  # 마우스 위아래 버튼 아래
            if block is not None:
                for i in range(len(block)):
                    if block[i].col_left < event.x < block[i].col_right:
                        if block[i].col_bottom < get_canvas_height() - event.y < block[i].col_top:
                            game_world.remove_object(block[i])
                            del (block[i])
                            break


def update():
    for game_object in game_world.all_objects():
        game_object.update()


def draw():
    clear_canvas()
    for game_object in game_world.all_objects():
        game_object.draw()
    ui.draw()
    update_canvas()
