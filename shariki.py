from my_lib import Vector2D
from math import sqrt
from random import randrange as rnd
import time
import tkinter as tk


# ---------------------------------------------------------------------------------------------------------------

class Wall:
    def __init__(self, normal, position=Vector2D()):
        self.n = normal
        self.p = position

    def __str__(self):
        return "Wall {{ position = {0}, normal = {1} }}".format(self.p, self.n)


class Round:
    def __init__(self, radius, position=Vector2D()):
        self.p = position
        self.r = radius

    def __str__(self):
        return "Round {{ radius = {0}, position = {1} }}".format(self.r, self.p)

    def __and__(self, other):
        if isinstance(other, Wall):
            return abs((self.p - other.p) * other.n) / abs(other.n) <= self.r
        else:
            raise ValueError("Я не умею проверять столкновение {0} и {1}".format(self, other))

    def __rand__(self, other):
        return self.__and__(other)

    def check(self, x, y):
        return abs(self.p - Vector2D( x, y)) <= self.r


class SolidBody:
    def __init__(self, velocity=Vector2D()):
        self.v = velocity

    @staticmethod
    def collide(b1, b2):
        if isinstance(b1, Round) and isinstance(b2, Wall):
            vp = (b1.v * b2.n) / abs(b2.n) ** 2 * b2.n  # параллельный нормали
            b1.v -= 2 * vp
        elif isinstance(b1, Wall) and isinstance(b2, Round):
            collide(b2, b1)
        else:
            raise ValueError("Я не умею вычислять столкновение {0} и {1}".format(self, other))

        # --------------------------------------relise--------------------------------------------------------------------------


# --------------------------------------inputs--------------------------------------------------------------------------
root = tk.Tk()
fr = tk.Frame(root)
root.geometry('800x600')
canv = tk.Canvas(root, bg='white')
canv.pack(fill=tk.BOTH, expand=1)
sky = canv.create_rectangle(0, 0, 800, 566, fill='lightblue')
ground = canv.create_rectangle(0, 566, 800, 600, fill='green')
screen1 = canv.create_text(400, 30, text='', font='28')

min_width = 30
max_width = 100

bullets = []


# -------------------------------------class_system---------------------------------------------------------------------

class SolidRound(Round, SolidBody):
    def __init__(self, color, radius, position=Vector2D(), velocity=Vector2D()):
        Round.__init__(self, radius, position)
        SolidBody.__init__(self, velocity)

        self.id = canv.create_oval(
            self.p.x - self.r,
            self.p.y - self.r,
            self.p.x + self.r,
            self.p.y + self.r
        )
        canv.itemconfig(self.id, fill=color)

    def __str__(self):
        return "SolidRound {{ radius = {0}, position = {1}, velocity = {2} }}".format(self.r, self.p, self.v)

    def update(self, delta_time=1):
        dp = delta_time * self.v
        self.p += dp
        canv.move(self.id, dp.x, dp.y)

    def __eq__(self, other):
        if self is other:
            return True
        return self.id == other.id

    def remove(self, container):
        canv.delete(self.id)
        try:
            container.remove(self)
        except:
            pass



class Game():
    score = 0

    def mouse_up(self, event):
        for target in reversed(targets):
            if target.check(event.x, event.y):
                target.remove(targets)
                self.score += 1
                canv.itemconfigure(game.label, text=self.score)
                break

# -------------------------------------------------object_system---------------------------------------------------
game = Game()


targets = [
    SolidRound(
        "red",
        rnd(20, 50),
        Vector2D(rnd(100, 750), rnd(50, 500)),
        Vector2D(rnd(-200, 200) / 200, rnd(-200, 200) / 200)
    ) for i in range(20)
]

walls = [
    Wall(Vector2D(0, -1), Vector2D(0, 600 - 30)),
    Wall(Vector2D(0, 1), Vector2D(0, 0)),
    Wall(Vector2D(1, 0), Vector2D(0, 0)),
    Wall(Vector2D(-1, 0), Vector2D(800, 0))
]


# -----------------------------------------------------game_relise------------------------------------------------


def new_game(event=''):
    vrem9 = time.time()

    canv.bind('<ButtonRelease-1>', game.mouse_up)
    canv.create_text(700, 100, text="Try to get it",
                     justify=tk.CENTER, font="Verdana 14")
    canv.create_text(700, 130, text="YOUR SCORE:",
                     justify=tk.CENTER, font="Verdana 14")
    game.label = canv.create_text(700, 160, text=0,
                     justify=tk.CENTER, font="Verdana 14")


    while targets:
        for target in targets:
            target.update()

            for wall in walls:
                if target & wall:
                    SolidRound.collide(target, wall)

        if time.time() - vrem9 > 1:
            vrem9 = time.time()
            targets.append(SolidRound(
                "red",
                rnd(20, 50),
                Vector2D(rnd(100, 750), rnd(50, 500)),
                Vector2D(rnd(-200, 200) / 200, rnd(-200, 200) / 200)))
        canv.update()
        time.sleep(0.01)

try:
    new_game()
except Exception as e:
    print(e.args[0])
    # for printing error in window, not trashing codex