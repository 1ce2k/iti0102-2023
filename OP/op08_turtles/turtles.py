"""Meta-trees and meta-dragons with Turtle."""
from turtle import Turtle
from sys import setrecursionlimit

setrecursionlimit(10000)


def tree(length: int, origin=(0, 0)) -> None:
    """
    Write a recursive turtle program to draw a binary tree.

    Start with a trunk 200px tall.
    Each new branch should be 3/5 as big as its trunk.
    Minimum branch size is 5px.
    Move turtle with: t.forward(), t.left(), t.right(), tree()


    :param length: height of the trunk or leaf
    :param origin: starting point.
    """
    if length < 5:
        return
    t.penup()
    x, y = origin
    t.goto(x, y)
    t.pendown()
    t.forward(length)
    t.left(60)
    tree(round(length * 0.6), t.pos())
    t.right(120)
    tree(round(length * 0.6), t.pos())
    t.left(60)
    t.penup()
    t.goto(x, y)
    t.pendown()


def apply_dragon_rules(string: str) -> str:
    """
    Write a recursive function that replaces characters in string.

    Like so:
        "a" -> "aRbFR"
        "b" -> "LFaLb"
    apply_dragon_rules("a") -> "aRbFR"
    apply_dragon_rules("aa") -> "aRbFRaRbFR"
    apply_dragon_rules("FRaFRb") -> "FRaRbFRFRLFaLb"

    :param string: sentence with "a" and "b" characters that need to be replaced
    :return: new sentence with "a" and "b" characters replaced
    """
    if not string:
        return ''
    if string[0] == 'a':
        return "aRbFR" + apply_dragon_rules(string[1:])
    if string[0] == 'b':
        return "LFaLb" + apply_dragon_rules(string[1:])
    return string[0] + apply_dragon_rules(string[1:])


def curve(string: str, depth: int) -> None | str:
    """
    Recursively generate the next depth of rules.

    Calls apply_dragon_rules() function `depth` times.
    curve("Fa", 2) -> "FaRbFRRLFaLbFR"

    :param string: current instruction string
    :param depth: how many times the rules are applied
    :return: instructionset for drawing the dragon at iteration 'depth'
    """
    if depth == 0:
        return string
    return curve(apply_dragon_rules(string), depth - 1)


def format_curve(string: str) -> str:
    """
    Use recursions to remove  a  and  b  symbols from the instruction string.

    format_curve("Fa") -> "F"
    format_curve("FaRbFR") -> "FRFR"

    :param string: instruction string
    :return: clean instructions with only "F", "R", and "L" characters
    """
    if not string:
        return ''
    if string[0] in ('a', 'b'):
        return format_curve(string[1:])
    return string[0] + format_curve(string[1:])


def draw_dragon(string: str, length: float) -> None:
    """Draws the dragon by reading the string recursively.

    Use t.right(), t.left(), t.forward() and draw_dragon() to move turtle.
        L - means turn 90 degrees to left and go forward
        R - means turn 90 degrees to right and go forward
        F - means don't turn just go forward

    :param string: instructions left to process
    :param length: how many pixels to move forward, left or right
    """
    if not string:
        return
    if string[0] == 'L':
        t.left(90)
        t.forward(length)
    elif string[0] == 'R':
        t.right(90)
        t.forward(length)
    elif string[0] == 'F':
        t.forward(length)
    draw_dragon(string[1:], length)


def get_line_length(dragon_width: int, depth: int) -> float:
    """Return one Turtle step length if the width and depth are known."""
    return dragon_width / (2 ** (1 / 2)) ** depth


def save(turtle: Turtle) -> None:
    """Save the turtle graphic to file which can be opened with a image editor like GIMP."""
    turtle.ht()  # hide him
    turtle.getscreen().getcanvas().postscript(file='../../OP/op08_turtles/turtles.ps')


if __name__ == '__main__':

    t = Turtle()
    t.getscreen().bgcolor("#1c262b")
    t.color("#96004f")
    t.speed(0)
    t.pensize(1)
    t.left(90)
    # use this to draw the binary tree
    # tree(200)

    s = curve("Fa", 8)
    s = format_curve(s)
    line_length = get_line_length(100, 8)
    # use this to draw the dragon curve
    draw_dragon(s, line_length)

    save(t)
    t.getscreen().exitonclick()
