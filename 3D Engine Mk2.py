#stl and obj

from matrix_constants import *
from time import *

import numpy as np
import tkinter as tk
#Settings
width=2000
height=1000
focus = 500

#Setup
root = tk.Tk()
root.geometry(f"{width}x{height}")
screen=tk.Canvas(root)
screen.pack(expand=True, fill=tk.BOTH)

class Controller():
    def __init__(self, root, sprite_repository):
        root.bind("<Key>", self.action)
        root.bind("<B1-Motion>", self.mouse_down)

        self._sprite_repo = sprite_repository
        self._mouse_pos = (500,500)

    def action(self, event):
        if event.char == "f":
            global focus
            if focus > 3000:
                focus = 100
            else:
                focus += 100
            print(f"Focus={focus}")
        update_screen()

        if event.char == "w":
            for s in self._sprite_repo: s.translate_view((0,0,-15))
            for s in self._sprite_repo: s.translate_view((0,0,-15))
        if event.char == "a":
            for s in self._sprite_repo: s.translate_view((7,0,0))
        if event.char == "s":
            for s in self._sprite_repo: s.translate_view((0,0,15))
        if event.char == "d":
            for s in self._sprite_repo: s.translate_view((-7,0,0))

        if event.char == " ":
            for s in self._sprite_repo:
                if event.state & 1 << 0:
                    s.translate_view((0, 7, 0)) 
                else:
                    s.translate_view((0, -7, 0))

        if event.char == "e":
            for s in self._sprite_repo: s.rotate_view("Z", 3)
        if event.char == "q":
            for s in self._sprite_repo: s.rotate_view("Z", -3)

        




        if event.char == "r":
            for s in self._sprite_repo: s.rotate_sprite("X", 4)
        if event.char == "t":
            for s in self._sprite_repo: s.rotate_sprite("Y", 1)
        if event.char == "y":
            for s in self._sprite_repo: s.rotate_sprite("Z", -1)

    def mouse_down(self, event):
        
        x, y = event.x, event.y
        dx, dy = x-self._mouse_pos[0], y-self._mouse_pos[1]
        if abs(dx) + abs(dy) > 20:
            self._mouse_pos = (x,y)
        else:
            for s in self._sprite_repo: s.rotate_view("Y", dx*-0.3)
            for s in self._sprite_repo: s.rotate_view("X", dy*-0.3)
            self._mouse_pos = (x,y)
        #print((dx,dy))



class Sprite():
    def __init__(self, points):
        self.points = points
        self.size = len(self.points)
        self.orientation = (0,0,0)
        self._behind = False

    def set_points(self, points: list) -> None:
        self.points = points

    def get_points(self):
        return self.points

    def check_behind(self):
        for point in self.points:
            if point[2] < 0.01:
                return True
        return False
        

    def get_twoD(self):
        twoD = []
        for point in self.points:
            nx = focus * point[0] / (point[2])**1 ##dynamic multiplier? based on z itself
            ny = focus * point[1] / (point[2])**1
            p = ((nx+width/2, -(ny)+height/2))
            #print(f"p = {p}")
            twoD.append(p)
        return twoD

    def gett_twoD(self):
        twoD = []
        for point in self.points:
            theta = np.arctan2(point[0], point[2])
            phi = np.arctan2(point[1], point[2])
            nx = theta * focus 
            ny = phi * focus
            p = ((nx+width/2, -(ny)+height/2))
            twoD. append(p)
        return twoD

    def get_centre(self):
        sumx=0
        sumy=0
        sumz=0
        for point in self.points:
            sumx +=point[0]
            sumy += point[1]
            sumz += point[2]
        return (sumx/self.size, sumy/self.size, sumz/self.size)
        
    def translate_view(self, dp: tuple[int]) -> None:
        global player_pos 
        x,y,z = player_pos
        dx, dy, dz = dp
        player_pos = (player_pos[0]+dx, player_pos[1]+dy, player_pos[2]+dz)
        for n,point in enumerate(self.points):
            x,y,z = point
            self.points[n] = (x+dx,y+dy,z+dz)
        update_screen()

    def rotate_view(self, axis: str, da:int) -> None: #rotates with respect player
        for n,point in enumerate(self.points):
            x,y,z = point
            f=np.array([[x],[y],[z]])
            if axis == "X":
                e = (Rx(da)).dot(f)
            if axis == "Y":
                e = (Ry(da)).dot(f)
            if axis == "Z":
                e = (Rz(da)).dot(f)
            self.points[n] = (e[0,0] ,e[1,0],e[2,0])
        update_screen()


    def rotate_sprite(self, axis: str, da: int) -> None:
        self.orientation = (self.orientation[0]+da, self.orientation[1], self.orientation[2])
        c1,c2,c3 = self.get_centre()
        for n,point in enumerate(self.points):
            x,y,z = point
            x,y,z = x-c1, y-c2, z-c3,
            f=np.array([[x],[y],[z]])
            if axis == "X":
                e = (Rx(da)).dot(f)
            if axis == "Y":
                e = (Ry(da)).dot(f)
            if axis == "Z":
                e = (Rz(da)).dot(f)
            self.points[n] = (e[0,0] +c1 ,e[1,0] +c2,e[2,0]+c3)
        #print(self.points)
        update_screen()

class Axes(Sprite):
    def rotate_sprite(self, axis, da):
        return None


def make_bcube(length):


    points = [] 
    for x in (length, -length):
        for y in (length, -length):
            for z in (length, -length):
                points.append((x, y, z))
    return points

def make_cube(length, c):
    coordinates = [
        (c[0] - length, c[1] + length, c[2] + length),   # Back top left
        (c[0] - length, c[1] - length, c[2] + length),  # Back bottom left
        (c[0] + length, c[1] - length, c[2] + length),  # Back bottom right
        (c[0] + length, c[1] + length, c[2] + length),  # Back top right

        (c[0] + length, c[1] + length, c[2] - length),  # Front top right

        (c[0] + length, c[1] - length, c[2] - length),  # Front bottom right
        (c[0] + length, c[1] - length, c[2] + length),  # Back bottom right
        (c[0] + length, c[1] - length, c[2] - length),  # Front bottom right

        (c[0] - length, c[1] - length, c[2] - length),  # Front bottom left
        (c[0] - length, c[1] - length, c[2] + length),  # Back bottom left
        (c[0] - length, c[1] - length, c[2] - length),  # Front bottom left

        (c[0] - length, c[1] + length, c[2] - length),   # Front top left
        (c[0] - length, c[1] + length, c[2] + length),   # Back top left
        (c[0] - length, c[1] + length, c[2] - length),   # Front top left

        (c[0] + length, c[1] + length, c[2] - length),  # Front top right
        (c[0] + length, c[1] + length, c[2] + length),  # Back top right
    ]
    return coordinates

def draw_line(p1: tuple[int,int], p2: tuple[int,int]) -> None:
    x1, y1 = p1
    x2, y2 = p2
    screen.create_line(x1,y1,x2,y2)

def clear_screen():
    screen.delete("all")

def update_screen():
    global sprite_repository
    clear_screen()
    if True: #consecutive
        for sprite in sprite_repository:
            if sprite.check_behind() == False:
                for p in range(1,sprite.size):
                    draw_line(sprite.get_twoD()[p-1],sprite.get_twoD()[p])
                draw_line(sprite.get_twoD()[0],sprite.get_twoD()[sprite.size - 1])


square = Sprite([(100,-100,300), (100,100,300), (-100,100,100), (-100,-100,100)])
floor = Sprite([(-500,-100,1000), (500,-100,1000), (500,-100,0), (-500,-100,0)])
cube = Sprite(make_cube(100, (0, 0, 300)))
cube1 = Sprite(make_cube(100, (0, 0, 800)))
axes = Axes([(100,100,100), (1000,100,100), (100,100,100), (100,1000,100),(100,100,100), (100,100,1000)])
sprite_repository = [cube]

player_pos = (0,0,0) 

control = Controller(root, sprite_repository)
update_screen()
root.mainloop()



#each sprite handles its own points and applies the transformations to them
#excessive screen updating?

#player seems to be 400 in front of origin not with linear 2d transform