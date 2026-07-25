"""
file: parabola.py
Author: Yinan Gordon Liu
Date: 2026-7-23
==============================================
Description: A simple script to demonstrate the properties of a parabola.
"""

import math
from graphics import Canvas

CANVAS_WIDTH = 800
CANVAS_HEIGHT = 600
g = 9.8

def draw_the_parabola(canvas, start_x, start_y, speed, start_angle):
    time = 0
    dtime = 0.001


    x1 = start_x
    y1 = start_y
    speed_x = speed * math.cos(start_angle)
    speed_y = speed * math.sin(start_angle)

    while True:
        x2 = x1 + speed_x * dtime
        y2 = y1 + speed_y * dtime * (-1)
        speed_y = speed_y - g * dtime

        canvas.create_line(x1, y1, x2, y2)
        x1 = x2
        y1 = y2

        if y2 > CANVAS_HEIGHT or x2 > CANVAS_WIDTH:
            break

    canvas.mainloop()



def main():
    canvas = Canvas(CANVAS_WIDTH, CANVAS_HEIGHT, "Parabola Simulation")
    start_x = int(input("Enter the x-coordinate of the vertex of the parabola: "))
    start_y = int(input("Enter the y-coordinate of the vertex of the parabola: "))
    speed = float(input("Enter the speed of the object: "))
    start_angle_in_degree = float(input("Enter the launch angle (in degrees): "))
    start_angle = math.radians(start_angle_in_degree)

    canvas.create_text(400, 20, text="Parabola Simulation", font=("Arial", 16))

    # Draw the parabola
    draw_the_parabola(canvas, start_x, start_y, speed, start_angle)
    






if __name__ == "__main__":
    main()