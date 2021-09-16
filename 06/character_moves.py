from pico2d import *
import math

open_canvas()

grass = load_image('grass.png')
character = load_image('character.png')

# fill here
state = 0
radian = 270

# character pos
x, y = 400, 90



while True:
    clear_canvas_now()
    grass.draw_now(400, 30)
    character.draw_now(x, y)
    delay(0.01)
    
    if state == 0:
        x += 10
        if x > 750:
            state = 1      

    elif state == 1:
        y += 10
        if y > 550:
            state = 2            

    elif state == 2:
        x -= 10
        if x < 50:
            state = 3            

    elif state == 3:
        y -= 10
        if y < 90:
            state = 4            

    elif state == 4:
        x += 10
        if x > 400:
            state = 5            

    elif state == 5:
        x = math.cos(radian / 360 * 2 * math.pi) * 200 + 400
        y = math.sin(radian / 360 * 2 * math.pi) * 200 + 300
        radian += 2
        if radian > 630:
            state = 0
            radian = 270

    
    


