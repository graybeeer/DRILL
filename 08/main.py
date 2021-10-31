from pico2d import *


# Game object class here
class Grass:
    def __init__(self):  # 생성자
        self.image = load_image('grass.png')

    def draw(self):
        self.image.draw(400, 30)

    pass


class Mayreel:
    def __init__(self):  # 생성자
        self.image = load_image('grass.png')

    def draw(self):
        self.image.draw(400, 30)
    pass



def handle_events():
    global running
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False


# initialization code
open_canvas()

block = Grass()

running = True

# game main loop code

while running:
    handle_events()

    # Game Logic
    # grass 에 대한 상호작용

    # Game Drawing
    block.draw()

    update_canvas()
# finalization code
