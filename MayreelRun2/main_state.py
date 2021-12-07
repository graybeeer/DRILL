from pico2d import *

import game_framework
import game_world
import map_state
import server
from player import Player
from sky import Sky
from block import Block

name = "MainState"
sky = None

class UI:
    def __init__(self):
        self.font = load_font('ENCR10B.TTF', 16)

    def draw(self):
        self.font.draw(800, 600, '(%d,%d)' % (server.player_area_x, server.player_area_y), (0, 0, 0))
        self.font.draw(800, 700, '(%d,%d)' % (len(server.block), len(server.block_sleep)), (0, 0, 0))
def enter():
    global sky,ui
    sky = Sky()
    ui=UI()
    server.player = Player()
    game_world.add_objects(server.background, 1)
    game_world.add_objects(server.background_sleep, 1)
    game_world.add_object(server.player, 4)
    game_world.add_objects(server.block, 2)
    game_world.add_objects(server.block_sleep, 2)
    game_world.add_objects(server.monster, 3)
    for block in (server.block+server.block_sleep):
        block.block_update()
    pass


def exit():
    game_world.clear()
    del server.player


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
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_SPACE:
            game_framework.change_state(map_state)
        if server.player is not None:
            server.player.handle_event(event)


def update():
    for game_object in game_world.all_objects():
        game_object.update()


def draw():
    clear_canvas()
    sky.draw()
    #ui.draw()
    for game_object in game_world.all_objects():
        if -500 < game_object.x + server.cx < 2500 and -500 < game_object.y + server.cy < 1500:
            game_object.draw()
    update_canvas()
