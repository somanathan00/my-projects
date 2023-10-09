import random
from turtle import Turtle, Screen

screen = Screen()
screen.setup(width=500, height=400)
is_race_on =False
user_bet=screen.textinput(title="turtle game",prompt="which turtle will win? enter the color: ")
color = ["red", "green", "purple", "blue", "yellow", "pink"]
y_positions = [-70, -40, -10, 20, 50, 80]
all_turtle = []

for i in range(0, 6):
    new_turtle = Turtle(shape='turtle')
    new_turtle.penup()
    new_turtle.color(color[i])
    new_turtle.goto(x=-230, y=y_positions[i])
    all_turtle.append(new_turtle)
if user_bet:
    is_race_on=True

while is_race_on:
    for turtle in all_turtle:
        if turtle.xcor() > 230:
            is_race_on=False
            winning_color=turtle.pencolor()
            if winning_color==user_bet:
                print(f"you've won, the {winning_color} turtle is the winner")
            else:
                print(f"you've lost, the {winning_color} turtle is the winner")

        random_distance=random.randint(1, 10)
        turtle.forward(random_distance)


screen.exitonclick()