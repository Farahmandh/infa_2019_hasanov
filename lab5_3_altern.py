from my_lib import Vector2D
from math import sqrt
from random import randrange as rnd
import time
import tkinter as tk

#---------------------------------------------------------------------------------------------------------------

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
        if isinstance(other, Round):
            return abs(self.p - other.p) <= self.r + other.r
        elif isinstance(other, Wall):
            return abs((self.p - other.p) * other.n) / abs(other.n) <= self.r 
        else:
            raise ValueError("Я не умею проверять столкновение {0} и {1}".format(self, other))

    def __rand__(self, other):
        return self.__and__(other)


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


#--------------------------------------relise--------------------------------------------------------------------------

#--------------------------------------inputs--------------------------------------------------------------------------
root = tk.Tk()
fr = tk.Frame(root)
root.geometry('800x600')
canv = tk.Canvas(root, bg='white')
canv.pack(fill=tk.BOTH, expand=1)
sky = canv.create_rectangle(0,0,800,566, fill='lightblue')
ground = canv.create_rectangle(0,566,800,600, fill='green')
screen1 = canv.create_text(400,30, text='', font='28')

min_width = 30
max_width = 100

bullets = []

#-------------------------------------class_system---------------------------------------------------------------------

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


class Gun(SolidRound):
    def __init__(self, body_color, head_color, fired_color, thikness, radius, m, position=Vector2D(), velocity=Vector2D()):
        super().__init__(body_color, radius, position, velocity)
        self.head_color = head_color
        self.fired_color = fired_color
        self.width = abs(m)
        self.m = m / self.width
        pos = self.p + m
        self.fired = False
        self.head_id = canv.create_line(self.p.x, self.p.y, pos.x, pos.y, width=thikness, fill=self.head_color)

    def update(self, delta_time=1):
        super().update(delta_time)
        if self.fired:
            if self.width < max_width:
                self.width += 1
                p = self.p + self.width * self.m
                canv.coords(
                    self.head_id,
                    self.p.x, self.p.y,
                    p.x, p.y
                )
            canv.itemconfig(self.head_id, fill=self.fired_color)
        else:
            canv.itemconfig(self.head_id, fill=self.head_color)
        v = delta_time * self.v
        canv.move(self.head_id, v.x, v.y)


    def update_motion(self, event):
        m = Vector2D(event.x, event.y)
        m -= gun.p
        m /= abs(m)
        self.m = m.copy()
        m *= self.width
        p = self.p + m
        canv.coords(
            self.head_id,
            self.p.x, self.p.y,
            p.x, p.y
        )

    def mouse_down(self, event):
        self.fired = True

    def mouse_up(self, event):
        bullets.append(
            SolidRound(
                "yellow",
                5,
                self.p.copy(),
                0.1 * self.width * self.m
            )
        )
        self.width = min_width
        self.fired = False


    def key_down(self, event):
        if event.keycode == 39:
            self.v.x = 5
        if event.keycode == 37:
            self.v.x = -5
        if event.keycode == 40:
            self.v.y = 5
        if event.keycode == 38:
            self.v.y = -5

    def key_up(self, event):
        if event.keycode == 39:
            self.v.x = 0
        if event.keycode == 37:
            self.v.x = 0
        if event.keycode == 40:
            self.v.y = 0
        if event.keycode == 38:
            self.v.y = 0

#-------------------------------------------------object_system---------------------------------------------------

gun = Gun(
    "purple", "black", "orange",
    10,
    20,
    Vector2D(min_width, 0),
    Vector2D(30, 450)
)

targets = [
    SolidRound(
        "red",
        rnd(20, 50),
        Vector2D(rnd(100, 750), rnd(50, 500)),
        Vector2D(rnd(-200,200)/200, rnd(-200,200)/200)
    ) for i in range(20)
]

walls = [
    Wall(Vector2D(0, -1), Vector2D(0, 600 - 30)),
    Wall(Vector2D(0, 1), Vector2D(0, 0)),
    Wall(Vector2D(1, 0), Vector2D(0, 0)),
    Wall(Vector2D(-1, 0), Vector2D(800, 0))
]


#-----------------------------------------------------game_relise------------------------------------------------

def new_game(event=''):
    root.bind('<KeyPress>', gun.key_down)
    root.bind('<KeyRelease>', gun.key_up)
    canv.bind('<Button-1>', gun.mouse_down)
    canv.bind('<ButtonRelease-1>', gun.mouse_up)
    canv.bind('<Motion>', gun.update_motion)
    
    while targets:
        #canv.itemconfig(screen1, text='You have used ' + str(bullet) + ' bullets to hit ' + str(points) + ' target')
        # g1.moveg()
        # for b in balls:
        #     b.move()
        #     for i in range(0,TARG):
        #         if b.hittest(t1,i) and (t1.live>0):
        #             LIVE -= 1
        #             t1.hit(i)
            #canv.bind('<Button-1>', '')
            #canv.bind('<ButtonRelease-1>', '')

        for wall in walls:
            if gun & wall:
            	m = (gun.v * wall.n) / abs(wall.n) ** 2
            	if m < 0:
	                vp = (gun.v * wall.n) / abs(wall.n) ** 2 * wall.n  # параллельный нормали
	                gun.v -= vp
        gun.update()

        for bullet in bullets:
            bullet.v.y += 0.1
            bullet.update()

            for wall in walls:
                if bullet & wall:
                    SolidRound.collide(bullet, wall) 

        bullets_to_remove = []
        targets_to_remove = []
        for target in targets:
            target.update()

            for wall in walls:
                if target & wall:
                    SolidRound.collide(target, wall)

            for bullet in bullets:
                # if bullet & walls[0]:
                #     bullets_to_remove.append(bullet)
                if bullet & target:
                    targets_to_remove.append(target)
                    bullets_to_remove.append(bullet)

            if target & gun:
                return

        for target in targets_to_remove:
            target.remove(targets)

        for bullet in bullets_to_remove:
            bullet.remove(bullets)

        # canv.itemconfig(screen1, text='You have used ' + str(bullet) + ' bullets to hit ' + str(points) + ' target')
        canv.update()
        time.sleep(0.01)
        # g1.targetting()
        # g1.power_up()
        #canv.itemconfig(screen1, text='You have used ' + str(bullet) + ' bullets to hit ' + str(points) + ' target)
    # canv.delete(gun)
    # root.after(750, new_game)

try:
    new_game()
except Exception as e:
    print(e.args[0])
    #for printing error in window, not trashing code
