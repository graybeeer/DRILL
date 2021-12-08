from pico2d import *

import game_framework
import game_world
import map_state
import server
import start_state
from player import Player
from sky import Sky
from block import Block

name = "MainState"
sky = None

class UI:
    def __init__(self):
        self.font = load_font('ENCR10B.TTF', 16)
        self.bgm = load_wav('bgm_burywood_main.wav')
        self.bgm.set_volume(64)
        self.bgm.repeat_play()

    def draw(self):
        self.font.draw(800, 600, '(%d,%d)' % (server.player_area_x, server.player_area_y), (0, 0, 0))
        self.font.draw(800, 700, '(%d,%d)' % (len(server.block), len(server.block_sleep)), (0, 0, 0))




def enter():
    global sky,ui
    sky = Sky()
    ui=UI()
    ui.bgm.repeat_play()
    server.player = Player()
    game_world.add_objects(server.background, 1)
    game_world.add_objects(server.background_sleep, 1)
    game_world.add_objects(server.block, 2)
    game_world.add_objects(server.block_sleep, 2)
    game_world.add_objects(server.monster, 3)
    game_world.add_object(server.player, 4)
    for block in (server.block+server.block_sleep):
        block.block_update()
    pass


def exit():
    ui.bgm.play(-1)
    game_world.clear()


def pause():
    pass


def resume():
    pass


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.change_state(start_state)
        elif event.type == SDL_KEYDOWN and event.key == SDLK_SPACE:
            game_framework.change_state(map_state)
        if server.player is not None:
            server.player.handle_event(event)
        else:
            pass


def update():
    for game_object in game_world.all_objects():
        game_object.update()


def draw():
    clear_canvas()
    sky.draw()
    #ui.draw()
    for game_object in game_world.all_objects():
        game_object.draw()
    update_canvas()
