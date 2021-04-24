import turtle
from triangle import Triangle

turtle.speed("fastest")
turtle.tracer(0)
turtle.hideturtle()

# turtle.colormode(255)


def update():
    turtle.update()


def offset_goto(coords):
    turtle.goto(coords[0] - (ScreenWidth() / 2), coords[1] - (ScreenHeight() / 2))


def draw_triangle(t: Triangle, debug: bool = False):
    # print(f"Drawn: {Triangle} with Debug set to {debug}")
    turtle.color(t.color, t.color)
    if debug:
        turtle.color((0, 0, 0), t.color)
    turtle.penup()
    offset_goto(t.p[0].coords2d())
    turtle.pendown()
    turtle.begin_fill()
    for p in t.p:
        offset_goto(p.coords2d())
    turtle.end_fill()


def ScreenHeight():
    return turtle.screensize()[0]*2


def ScreenWidth():
    return turtle.screensize()[1]*3


def clear():
    turtle.clear()


def exitonclick():
    turtle.exitonclick()
