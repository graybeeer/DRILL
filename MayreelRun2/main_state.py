from pico2d import *

import game_framework
import game_world
import map_state
import server
from player import Player
from sky import Sky
name = "MainState"


def enter():
    server.sky = Sky()
    server.player = Player()
    game_world.add_object(server.sky, 0)
    game_world.add_object(server.player, 2)
    game_world.add_objects(server.block, 1)

    pass


def exit():
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
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_SPACE:
            game_framework.change_state(map_state)
        server.player.handle_event(event)


def update():
    for game_object in game_world.all_objects():
        game_object.update()



def draw():
    clear_canvas()
    for game_object in game_world.all_objects():
        if -500 < game_object.x+server.cx < 2500 and -500 < game_object.y+server.cy < 1500:
            game_object.draw()
    update_canvas()
