import turtle

a=0
b=0
c=0
while(c<5):
    while(b<5):
        
        turtle.penup()
        turtle.goto(b*100-300,c*100-300)
        turtle.pendown()

        while(a<4):
            turtle.forward(100)
            turtle.left(90)
            a+=1
        a=0
        b+=1  
    b=0
    c+=1

turtle.exitonclick()
