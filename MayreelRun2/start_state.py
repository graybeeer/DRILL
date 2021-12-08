from pico2d import *

import game_framework
import main_state
import map_state

name = "StartState"
start_menu = None
game_ui = False


class StartMenu:
    def __init__(self):
        self.image = load_image('ui/start_menu.png')
        self.font = load_font('a시월구일3.ttf', 60)
        self.font_ui = load_font('a시월구일2.ttf', 30)
        self.image_ui = load_image('ui/whiteboard.png')

    def update(self):
        pass

    def draw(self):
        self.image.clip_draw(0, 0, self.image.w, self.image.h, 800, 450, 1600, 900)
        self.font.draw(1150, 730, '%s' % ("GAME START"), (0, 0, 0))
        self.font.draw(1150, 530, '%s' % ("MAP EDITOR"), (0, 0, 0))
        self.font.draw(1150, 330, '%s' % ("???"), (0, 0, 0))
        self.font.draw(1150, 130, '%s' % ("GAME QUIT"), (0, 0, 0))
        if game_ui==True:
            self.image_ui.clip_draw(0, 0, 100, 100, 800, 450, 1000, 600)
            for i in range(5):
                draw_rectangle(150 * i + 350, 400, 150 * i + 500, 550)
                self.font_ui.draw(150 * i + 375, 475, "월드" + "%d " % (i + 1), (0, 0, 0))
            for i in range(5):
                draw_rectangle(150 * i + 350, 200, 150 * i + 500, 350)
                self.font_ui.draw(150 * i + 375, 275, "월드" + "%d " % (i + 6), (0, 0, 0))



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
    global game_ui
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_ui = False
        if (event.type, event.button) == (SDL_MOUSEBUTTONDOWN, SDL_BUTTON_LMASK):
            if 1100 < event.x < 1600:
                if 650 < get_canvas_height() - event.y < 800:
                    game_ui = True
                elif 450 < get_canvas_height() - event.y < 600:
                    game_framework.change_state(map_state)
                elif 50 < get_canvas_height() - event.y < 200:
                    game_framework.quit()


def update():
    pass


def draw():
    clear_canvas()
    start_menu.draw()
    update_canvas()
