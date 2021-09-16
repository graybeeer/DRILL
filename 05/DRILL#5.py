import turtle

def w_move():
    turtle.setheading(90)
    turtle.forward(50)
    turtle.stamp()

def a_move():
    turtle.setheading(180)
    turtle.forward(50)
    turtle.stamp()

def s_move():
    turtle.setheading(270)
    turtle.forward(50)
    turtle.stamp()

def d_move():
    turtle.setheading(0)
    turtle.forward(50)
    turtle.stamp()

def restart():
    turtle.reset()

turtle.shape('turtle')
turtle.onkey(w_move,'W')
turtle.onkey(a_move,'A')
turtle.onkey(s_move,'S')
turtle.onkey(d_move,'D')
turtle.onkey(restart,'Escape')
turtle.listen()
