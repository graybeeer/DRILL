import random
import turtle
import math


def stop():
    turtle.bye()


def prepare_turtle_canvas():
    turtle.setup(1024, 768)
    turtle.bgcolor(0.2, 0.2, 0.2)
    turtle.penup()
    turtle.hideturtle()
    turtle.shape('arrow')
    turtle.shapesize(2)
    turtle.pensize(5)
    turtle.color(1, 0, 0)
    turtle.speed(100)
    turtle.goto(-500, 0)
    turtle.pendown()
    turtle.goto(480, 0)
    turtle.stamp()
    turtle.penup()
    turtle.goto(0, -360)
    turtle.pendown()
    turtle.goto(0, 360)
    turtle.setheading(90)
    turtle.stamp()
    turtle.penup()
    turtle.home()

    turtle.shape('circle')
    turtle.pensize(1)
    turtle.color(0, 0, 0)
    turtle.speed(50)

    turtle.onkey(stop, 'Escape')
    turtle.listen()


def draw_big_point(p):
    turtle.goto(p)
    turtle.color(0.8, 0.9, 0)
    turtle.dot(15)
    turtle.write('     ' + str(p))


def draw_point(p):
    turtle.goto(p)
    turtle.dot(5, random.random(), random.random(), random.random())


def draw_line_basic(p1, p2):
    draw_big_point(p1)
    draw_big_point(p2)

    x1, y1 = p1
    x2, y2 = p2

    직선_기울기 = (y2 - y1) / (x2 - x1)
    y의_절편 = y1 - x1 * 직선_기울기

    for x in range(x1, x2 + 1, 10):
        y = 직선_기울기 * x + y의_절편
        draw_point((x, y))

    draw_point(p2)
    pass


def draw_circle(p1, p2):
    draw_big_point(p1)
    draw_big_point(p2)

    x1, y1 = p1
    x2, y2 = p2

    점_거리 = math.dist(p1, p2)

    for 각도 in range(0, 360, 5):
        x = math.cos(각도 * math.pi / 180) * 점_거리 / 2 + (x1 + x2) / 2
        y = math.sin(각도 * math.pi / 180) * 점_거리 / 2 + (y1 + y2) / 2
        draw_point((x, y))

    draw_point(p1)
    draw_point(p2)
    pass

def draw_shape():
    a = 340
    b = 200
    t = 0.0
    while t <= 32 * math.pi:
        x = (a - b) * math.cos(t) + b * math.cos(t * (a / b - 1))
        y = (a - b) * math.sin(t) - b * math.sin(t * (a / b - 1))
        t += (math.pi / 20)
        draw_point((x, y))
    pass
prepare_turtle_canvas()


#draw_circle(q1, q2)

draw_shape()
turtle.done()
