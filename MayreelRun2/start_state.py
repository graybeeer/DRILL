from pico2d import *

import game_framework
import main_state
import map_state

name = "StartState"
start_menu = None


class StartMenu:
    def __init__(self):
        self.image = load_image('ui/start_menu.png')
        self.font = load_font('a시월구일3.ttf', 60)

    def update(self):
        pass

    def draw(self):
        self.image.clip_draw(0, 0, self.image.w, self.image.h, 800, 450, 1600, 900)
        self.font.draw(1150, 730, '%s' % ("GAME START"), (0, 0, 0))
        self.font.draw(1150, 530, '%s' % ("MAP EDITOR"), (0, 0, 0))


def enter():
    global start_menu
    start_menu = StartMenu()
    pass


def exit():
    global start_menu
    del start_menu


def pause():
    pass


def resume():
    pass


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        if (event.type, event.button) == (SDL_MOUSEBUTTONDOWN, SDL_BUTTON_LMASK):
            if 1100 < event.x < 1600:
                if 650 < get_canvas_height() - event.y < 750:
                    game_framework.change_state(main_state)
                elif 450 < get_canvas_height() - event.y < 550:
                    game_framework.change_state(map_state)


def update():
    pass


def draw():
    clear_canvas()
    start_menu.draw()
    update_canvas()
