from graph import *
from math import *


deg2rad = pi / 180

time = 0

def draw_hair(x, y, r, R, alpha, n, da):
    alpha *= deg2rad
    da *= deg2rad
    alpha -= n * da
    point = []
    for i in range(2 * n + 1):
        if i % 2 == 0:
            point.append((x + r * cos(alpha), y + r * sin(alpha)))
        else:
            point.append((x + R * cos(alpha), y + R * sin(alpha)))
        alpha += da
    point.append(point[0])
    polygon(point)

def draw_pentagram(x, y, a, alpha):
    #alpha *= deg2rad
    points = []
    for i in range(5):
        points.append((x + a * cos(alpha), y + a * sin(alpha)))
        alpha += 72 * deg2rad
    polygon(points)

def draw_hand( x, y, l, beta ):
    beta *= deg2rad
    # руки
    penSize(20)
    penColor(254, 190, 21)
    line(x , y, x + l*sin(beta), y + l*cos(beta))


    # кисть
    penSize(1)
    brushColor(254, 190, 21)
    penColor(255, 234, 0)
    circle(x + l*sin(beta), y + l*cos(beta), 0.15*l)

    # рукав
    penSize(1)
    penColor(0, 0, 0)
    brushColor(255, 39, 0)

    draw_pentagram(x, y, 0.2 * l, 0.1 - beta)




def draw_man(x0, y0, Rg, Rh, color1, color2, color3):
    #  n, ne, e, se, s, sw, w, nw, or center
    # brushColor("green")
    # rectangle( 0, 0, 500, 50)


    global time

    S = 20*(sin(time/20) + 1 )

    brushColor(color1)
    draw_hair(x0, y0, Rg, Rh, -90, 9, 8)

    # одежда
    brushColor(color2)
    circle(x0, y0 + Rg / 125 * 200, 1.1 * Rg)
    # polygon(((120, 350), (140, 330), (160, 350), (160, 370), (140, 370), (120, 350)))
    # polygon(((380, 350), (360, 330), (340, 350), (340, 370), (360, 370), (380, 350)))

    # голова
    penColor(254, 190, 21)
    brushColor(254, 190, 21)
    circle(x0, y0, Rg)



    # руки
    #penSize(20)
    #penColor(254, 190, 21)
    #line(x0 - Rg / 125 * 120, y0 + Rg / 125 * 110, x0 - Rg / 125 * 190, y0 - Rg / 125 * 150)
    #line(x0 + Rg / 125 * 120, y0 + Rg / 125 * 110, x0 + Rg / 125 * 190, y0 - Rg / 125 * 150)

    # рукава
    #penSize(1)
    #penColor(0, 0, 0)
    #brushColor(255, 39, 0)

    #draw_pentagram(x0 - Rg / 125 * 120, y0 + Rg / 125 * 110, 0.32 * Rg, S)
    #draw_pentagram(x0 + Rg / 125 * 120, y0 + Rg / 125 * 110, 0.32 * Rg, 180 - S)

    # нос
    brushColor("brown")
    polygon(((x0 - Rg / 125 * 10, y0 + Rg / 125 * 20), (x0 + Rg / 125 * 10, y0 + Rg / 125 * 20),
             (x0, y0 + Rg / 125 * 30), (x0 - Rg / 125 * 10, y0 + Rg / 125 * 20)))

    # рот
    brushColor("red")
    polygon(((x0 - Rg / 125 * 50, y0 + Rg / 125 * 50), (x0 + Rg / 125 * 50, y0 + Rg / 125 * 50),
             (x0, y0 + Rg / 125 * 90), (x0 - Rg / 125 * 50, y0 + Rg / 125 * 50)))

    # кисть
    #brushColor(254, 190, 21)
    #penColor(255, 234, 0)
    #circle(x0 - Rg / 125 * 190, y0 - Rg / 125 * 150, 0.2 * Rg)
    #circle(x0 + Rg / 125 * 190, y0 - Rg / 125 * 150, 0.2 * Rg)

    # глаза
    brushColor(color3)
    penColor("black")
    circle(x0 - Rg / 125 * 40, y0 - Rg / 125 * 30, 0.2 * Rg)
    circle(x0 + Rg / 125 * 40, y0 - Rg / 125 * 30, 0.2 * Rg)
    brushColor("black")
    circle(x0 - Rg / 125 * 40, y0 - Rg / 125 * 30, 0.048 * Rg)
    circle(x0 + Rg / 125 * 40, y0 - Rg / 125 * 30, 0.048 * Rg)

    draw_hand(x0 - Rg / 125 * 120, y0 + Rg / 125 * 110, 2 * Rg, S + 180 )
    draw_hand(x0 + Rg / 125 * 120, y0 + Rg / 125 * 110, 2 * Rg, -S+ 180)

    time = time +1
def draw_mans():
    brushColor( 255, 255, 255)
    rectangle( 0, 0, 1000, 600)
    label("Python is really amazing!", 20, 30, width=20, fg="yellow", bg="green", font="Arial 30")
    draw_man(130, 250, 75, 85, "red", "black", "orange")
    draw_man(370, 250, 75, 85, "blue", "green", "orange")
# windowSize(1000, 600)


onTimer(draw_mans, 50)

run()