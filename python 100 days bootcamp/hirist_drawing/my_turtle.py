import random
import turtle as t
import colorgram
t.colormode(255)
timy= t.Turtle()
timy.speed("fastest")
color_list=[]
color = colorgram.extract("image.jpg",10)
for c in color:
    r = c.rgb.r
    g = c.rgb.g
    b = c.rgb.b
    new_color = (r, g, b)
    color_list.append(new_color)


timy.penup()
timy.hideturtle()
timy.setheading(225)
timy.forward(300)
timy.setheading(0)

num_of_dots = 100
for dot_count in range(1, num_of_dots+1):
    timy.setheading(0)
    timy.dot(20,random.choice(color_list))
    timy.forward(50)

    if dot_count % 10 == 0:
        timy.setheading(90)
        timy.forward(50)
        timy.setheading(180)
        timy.forward(500)

t.exitonclick()