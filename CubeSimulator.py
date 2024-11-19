import pygame
import sys
import kociemba as ko
from tkinter import *
from threading import Thread
from tkinter.messagebox import *
import time
import random

class ColorBlock:
    def __init__(self, color, pol, type):
        self.color = color
        if type == "F":
            self.points = [(pol[0], pol[1]),\
                           (pol[0] + 99, pol[1] + 12),\
                           (pol[0] + 99, pol[1] + 112),\
                           (pol[0], pol[1] + 100)]
        elif type == "U":
            self.points = [(pol[0], pol[1]),\
                           (pol[0] + 99, pol[1] + 12),\
                           (pol[0] + 62, pol[1] + 49),\
                           (pol[0] - 37, pol[1] + 37)]
        elif type == "R":
            self.points = [(pol[0], pol[1]),\
                           (pol[0] + 37, pol[1] - 37),\
                           (pol[0] + 37, pol[1] + 63),\
                           (pol[0], pol[1] + 100)]
        else:
            raise TypeError

class Cube:
    def __init__(self):
        """
        up = White, front = green, when program use scamble
        else, up = yellow, front = blue
        the string is made up with the chars from up, right, front, down, left, back
        """
        self.faces = ["R", "L", "U", "D", "F", "B"]
        self.middles = ["M", "S", "E"]
        self.alls = ["x", "y", "z"]
        self.towLayers = ["r", "u", "l", "d", "f", "b"]

        self.UP = ["U"] * 9
        self.RIGHT = ["R"] * 9
        self.FRONT = ["F"] * 9
        self.DOWN = ["D"] * 9
        self.LEFT = ["L"] * 9
        self.BACK = ["B"] * 9

        self.cx = 150
        self.cy = 100

        
        self.COLORS = {"white":(255, 255, 255), "black":(0, 0, 0), "pink":(255, 174, 201), "yellow":(242, 255, 24),\
                  "blue":(8, 115, 255), "orange":(255, 138, 0), "red":(255, 0, 0), "green":(47, 201, 108),\
                  "U":(255, 255, 255), "D":(242, 255, 24), "L":(255, 138, 0), "R":(255, 0, 0),\
                  "B":(8, 115, 255), "F":(47, 201, 108)}

        self.displayblocks = []
        self.displaypositions = [[[111, 0], [210, 12], [309, 24],\
                                  [74, 37], [173, 49], [272, 61],\
                                  [37, 74], [136, 86], [235, 98]],\
                                 [[297, 147], [334, 110], [371, 73],\
                                  [297, 247], [334, 210], [371, 173],\
                                  [297, 347], [334, 310], [371, 273]],\
                                 [[0, 111], [99, 123], [198, 135],\
                                  [0, 211], [99, 223], [198, 235],\
                                  [0, 311], [99, 323], [198, 335]]]
        self.lineps = [[[111, 0], [0, 111]], [[210, 12], [99, 123]], [[309, 24], [198, 135]], [[408, 36], [297, 147]],\
                       [[111, 0], [408, 36]], [[74, 37], [371, 73]], [[37, 74], [334, 110]], [[0, 111], [297, 147]],\
                       [[0, 211], [297, 247]], [[0, 311], [297, 347]], [[0, 411], [297, 447]],\
                       [[0, 111], [0, 411]], [[99, 123], [99, 423]], [[198, 135], [198, 435]], [[297, 147], [297, 447]],\
                       [[297, 247], [408, 136]], [[297, 347], [408, 236]], [[297, 447], [408, 336]],\
                       [[334, 110], [334, 410]], [[371, 73], [371, 373]], [[408, 36], [408, 336]]]
        for i in self.displaypositions:
            for j in i:
                j[0] += self.cx
                j[1] += self.cy
        for i in self.lineps:
            i[0][0] += self.cx
            i[0][1] += self.cy
            i[1][0] += self.cx
            i[1][1] += self.cy

        for i in range(9):
            self.displayblocks.append(ColorBlock(self.COLORS["white"], self.displaypositions[0][i], "U"))
        for i in range(9):
            self.displayblocks.append(ColorBlock(self.COLORS["red"], self.displaypositions[1][i], "R"))
        for i in range(9):
            self.displayblocks.append(ColorBlock(self.COLORS["green"], self.displaypositions[2][i], "F"))

    def allreset(self): 
        # 还原，然后坐标系黄顶蓝前
        # 理论上应该白顶绿前，但是为了美观微调一下
        self.UP = ["U"] * 9
        self.RIGHT = ["R"] * 9
        self.FRONT = ["F"] * 9
        self.DOWN = ["D"] * 9
        self.LEFT = ["L"] * 9
        self.BACK = ["B"] * 9
        self.turn("x", 0)

    def xyzstd(self): # 整体坐标系变成白顶绿前，求解时用
        for i in range(4):
           if self.UP[4]!= "U":
               self.turn("x", 1)
        while self.UP[4] != "U":
            self.turn("z", 1)
        while self.FRONT[4] != "F":
            self.turn("y", 1)
        self.flushcolors()

    def blockreset(self): # 坐标系不变，原地还原
        self.UP = [self.UP[4]] * 9
        self.DOWN = [self.DOWN[4]] * 9
        self.LEFT = [self.LEFT[4]] * 9
        self.RIGHT = [self.RIGHT[4]] * 9
        self.FRONT = [self.FRONT[4]] * 9
        self.BACK = [self.BACK[4]] * 9
        self.flushcolors()

    def faceTurn90(self, dire, clockwise):
        # dire is like "R", "U" and so on
        # direction is like self.UP and so on
        # clockwise is True or False
        # R -> clockwise=T  R' -> clockwise=F
        if dire == "U":
            # 面上8格自旋转
            self.UP = self.UP[6::-3]+self.UP[7::-3]+self.UP[8::-3]\
                if clockwise else self.UP[2::3]+self.UP[1::3]+self.UP[::3]
            # 4个侧面涉及到的色块交换
            if clockwise:
                self.FRONT[0], self.RIGHT[0], self.BACK[0], self.LEFT[0] = self.RIGHT[0], self.BACK[0], self.LEFT[0], self.FRONT[0]
                self.FRONT[1], self.RIGHT[1], self.BACK[1], self.LEFT[1] = self.RIGHT[1], self.BACK[1], self.LEFT[1], self.FRONT[1]
                self.FRONT[2], self.RIGHT[2], self.BACK[2], self.LEFT[2] = self.RIGHT[2], self.BACK[2], self.LEFT[2], self.FRONT[2]
            else:
                self.FRONT[0], self.RIGHT[0], self.BACK[0], self.LEFT[0] = self.LEFT[0], self.FRONT[0], self.RIGHT[0], self.BACK[0]
                self.FRONT[1], self.RIGHT[1], self.BACK[1], self.LEFT[1] = self.LEFT[1], self.FRONT[1], self.RIGHT[1], self.BACK[1]
                self.FRONT[2], self.RIGHT[2], self.BACK[2], self.LEFT[2] = self.LEFT[2], self.FRONT[2], self.RIGHT[2], self.BACK[2]
        elif dire == "D":
            self.DOWN = self.DOWN[6::-3]+self.DOWN[7::-3]+self.DOWN[8::-3]\
                if clockwise else self.DOWN[2::3]+self.DOWN[1::3]+self.DOWN[::3]
            if clockwise:
                self.FRONT[6], self.RIGHT[6], self.BACK[6], self.LEFT[6] = self.LEFT[6], self.FRONT[6], self.RIGHT[6], self.BACK[6]
                self.FRONT[7], self.RIGHT[7], self.BACK[7], self.LEFT[7] = self.LEFT[7], self.FRONT[7], self.RIGHT[7], self.BACK[7]
                self.FRONT[8], self.RIGHT[8], self.BACK[8], self.LEFT[8] = self.LEFT[8], self.FRONT[8], self.RIGHT[8], self.BACK[8]
            else:
                self.FRONT[6], self.RIGHT[6], self.BACK[6], self.LEFT[6] = self.RIGHT[6], self.BACK[6], self.LEFT[6], self.FRONT[6]
                self.FRONT[7], self.RIGHT[7], self.BACK[7], self.LEFT[7] = self.RIGHT[7], self.BACK[7], self.LEFT[7], self.FRONT[7]
                self.FRONT[8], self.RIGHT[8], self.BACK[8], self.LEFT[8] = self.RIGHT[8], self.BACK[8], self.LEFT[8], self.FRONT[8]
        elif dire == "R":
            self.RIGHT = self.RIGHT[6::-3]+self.RIGHT[7::-3]+self.RIGHT[8::-3]\
                if clockwise else self.RIGHT[2::3]+self.RIGHT[1::3]+self.RIGHT[::3]
            if clockwise:
                self.UP[2], self.BACK[6], self.DOWN[2], self.FRONT[2] = self.FRONT[2], self.UP[2], self.BACK[6], self.DOWN[2]
                self.UP[5], self.BACK[3], self.DOWN[5], self.FRONT[5] = self.FRONT[5], self.UP[5], self.BACK[3], self.DOWN[5]
                self.UP[8], self.BACK[0], self.DOWN[8], self.FRONT[8] = self.FRONT[8], self.UP[8], self.BACK[0], self.DOWN[8]
            else:
                self.UP[2], self.BACK[6], self.DOWN[2], self.FRONT[2] = self.BACK[6], self.DOWN[2], self.FRONT[2], self.UP[2]
                self.UP[5], self.BACK[3], self.DOWN[5], self.FRONT[5] = self.BACK[3], self.DOWN[5], self.FRONT[5], self.UP[5]
                self.UP[8], self.BACK[0], self.DOWN[8], self.FRONT[8] = self.BACK[0], self.DOWN[8], self.FRONT[8], self.UP[8]
        elif dire == "L":
            self.LEFT = self.LEFT[6::-3]+self.LEFT[7::-3]+self.LEFT[8::-3]\
                if clockwise else self.LEFT[2::3]+self.LEFT[1::3]+self.LEFT[::3]
            if clockwise:
                self.UP[0], self.BACK[8], self.DOWN[0], self.FRONT[0] = self.BACK[8], self.DOWN[0], self.FRONT[0], self.UP[0]
                self.UP[3], self.BACK[5], self.DOWN[3], self.FRONT[3] = self.BACK[5], self.DOWN[3], self.FRONT[3], self.UP[3]
                self.UP[6], self.BACK[2], self.DOWN[6], self.FRONT[6] = self.BACK[2], self.DOWN[6], self.FRONT[6], self.UP[6]
            else:
                self.UP[0], self.BACK[8], self.DOWN[0], self.FRONT[0] = self.FRONT[0], self.UP[0], self.BACK[8], self.DOWN[0]
                self.UP[3], self.BACK[5], self.DOWN[3], self.FRONT[3] = self.FRONT[3], self.UP[3], self.BACK[5], self.DOWN[3]
                self.UP[6], self.BACK[2], self.DOWN[6], self.FRONT[6] = self.FRONT[6], self.UP[6], self.BACK[2], self.DOWN[6]
        elif dire == "F":
            self.FRONT = self.FRONT[6::-3]+self.FRONT[7::-3]+self.FRONT[8::-3]\
                if clockwise else self.FRONT[2::3]+self.FRONT[1::3]+self.FRONT[::3]
            if clockwise:
                self.UP[6], self.RIGHT[0], self.DOWN[2], self.LEFT[8] = self.LEFT[8], self.UP[6], self.RIGHT[0], self.DOWN[2]
                self.UP[7], self.RIGHT[3], self.DOWN[1], self.LEFT[5] = self.LEFT[5], self.UP[7], self.RIGHT[3], self.DOWN[1]
                self.UP[8], self.RIGHT[6], self.DOWN[0], self.LEFT[2] = self.LEFT[2], self.UP[8], self.RIGHT[6], self.DOWN[0]
            else:
                self.UP[6], self.RIGHT[0], self.DOWN[2], self.LEFT[8] = self.RIGHT[0], self.DOWN[2], self.LEFT[8], self.UP[6]
                self.UP[7], self.RIGHT[3], self.DOWN[1], self.LEFT[5] = self.RIGHT[3], self.DOWN[1], self.LEFT[5], self.UP[7]
                self.UP[8], self.RIGHT[6], self.DOWN[0], self.LEFT[2] = self.RIGHT[6], self.DOWN[0], self.LEFT[2], self.UP[8]
        elif dire == "B":
            self.BACK = self.BACK[6::-3]+self.BACK[7::-3]+self.BACK[8::-3]\
                if clockwise else self.BACK[2::3]+self.BACK[1::3]+self.BACK[::3]
            if clockwise:
                self.UP[0], self.RIGHT[2], self.DOWN[8], self.LEFT[6] = self.RIGHT[2], self.DOWN[8], self.LEFT[6], self.UP[0]
                self.UP[1], self.RIGHT[5], self.DOWN[7], self.LEFT[3] = self.RIGHT[5], self.DOWN[7], self.LEFT[3], self.UP[1]
                self.UP[2], self.RIGHT[8], self.DOWN[6], self.LEFT[0] = self.RIGHT[8], self.DOWN[6], self.LEFT[0], self.UP[2]
            else:
                self.UP[0], self.RIGHT[2], self.DOWN[8], self.LEFT[6] = self.LEFT[6], self.UP[0], self.RIGHT[2], self.DOWN[8]
                self.UP[1], self.RIGHT[5], self.DOWN[7], self.LEFT[3] = self.LEFT[3], self.UP[1], self.RIGHT[5], self.DOWN[7]
                self.UP[2], self.RIGHT[8], self.DOWN[6], self.LEFT[0] = self.LEFT[0], self.UP[2], self.RIGHT[8], self.DOWN[6]
        else:
            raise TypeError("use error")
    
    def faceTurn180(self, dire):
        
        if dire == "U":
            self.UP[:4], self.UP[8:4:-1] = self.UP[8:4:-1], self.UP[:4]
            self.FRONT[:3], self.BACK[:3] = self.BACK[:3], self.FRONT[:3]
            self.LEFT[:3], self.RIGHT[:3] = self.RIGHT[:3], self.LEFT[:3]
        elif dire == "D":
            self.DOWN[:4], self.DOWN[8:4:-1] = self.DOWN[8:4:-1], self.DOWN[:4]
            self.FRONT[6:], self.BACK[6:] = self.BACK[6:], self.FRONT[6:]
            self.LEFT[6:], self.RIGHT[6:] = self.RIGHT[6:], self.LEFT[6:]
        elif dire == "L":
            self.LEFT[:4], self.LEFT[8:4:-1] = self.LEFT[8:4:-1], self.LEFT[:4]
            self.UP[::3], self.DOWN[::3] = self.DOWN[::3], self.UP[::3]
            self.FRONT[::3], self.BACK[8:1:-3] = self.BACK[8:1:-3], self.FRONT[::3]
        elif dire == "R":
            self.RIGHT[:4], self.RIGHT[8:4:-1] = self.RIGHT[8:4:-1], self.RIGHT[:4]
            self.UP[2::3], self.DOWN[2::3] = self.DOWN[2::3], self.UP[2::3]
            self.FRONT[2::3], self.BACK[6::-3] = self.BACK[6::-3], self.FRONT[2::3]
        elif dire == "F":
            self.FRONT[:4], self.FRONT[8:4:-1] = self.FRONT[8:4:-1], self.FRONT[:4]
            self.UP[6:], self.DOWN[2::-1] = self.DOWN[2::-1], self.UP[6:]
            self.RIGHT[::3], self.LEFT[8:1:-3] = self.LEFT[8:1:-3], self.RIGHT[::3]
        elif dire == "B":
            self.BACK[:4], self.BACK[8:4:-1] = self.BACK[8:4:-1], self.BACK[:4]
            self.UP[:3], self.DOWN[8:5:-1] = self.DOWN[8:5:-1], self.UP[:3]
            self.RIGHT[2::3], self.LEFT[6::-3] = self.LEFT[6::-3], self.RIGHT[2::3]
        else:
            raise ValueError("use error")
        self.flushcolors()

    def midTurn90(self, lay, clockwise):
        if lay == "M":
            if clockwise:
                self.UP[1], self.BACK[7], self.DOWN[1], self.FRONT[1] = self.BACK[7], self.DOWN[1], self.FRONT[1], self.UP[1]
                self.UP[4], self.BACK[4], self.DOWN[4], self.FRONT[4] = self.BACK[4], self.DOWN[4], self.FRONT[4], self.UP[4]
                self.UP[7], self.BACK[1], self.DOWN[7], self.FRONT[7] = self.BACK[1], self.DOWN[7], self.FRONT[7], self.UP[7]
            else:
                self.UP[1], self.BACK[7], self.DOWN[1], self.FRONT[1] = self.FRONT[1], self.UP[1], self.BACK[7], self.DOWN[1]
                self.UP[4], self.BACK[4], self.DOWN[4], self.FRONT[4] = self.FRONT[4], self.UP[4], self.BACK[4], self.DOWN[4]
                self.UP[7], self.BACK[1], self.DOWN[7], self.FRONT[7] = self.FRONT[7], self.UP[7], self.BACK[1], self.DOWN[7]
        elif lay == "S":
            if clockwise:
                self.UP[3], self.RIGHT[1], self.DOWN[5], self.LEFT[7] = self.LEFT[7], self.UP[3], self.RIGHT[1], self.DOWN[5]
                self.UP[4], self.RIGHT[4], self.DOWN[4], self.LEFT[4] = self.LEFT[4], self.UP[4], self.RIGHT[4], self.DOWN[4]
                self.UP[5], self.RIGHT[7], self.DOWN[3], self.LEFT[1] = self.LEFT[1], self.UP[5], self.RIGHT[7], self.DOWN[3]
            else:
                self.UP[3], self.RIGHT[1], self.DOWN[5], self.LEFT[7] = self.RIGHT[1], self.DOWN[5], self.LEFT[7], self.UP[3]
                self.UP[4], self.RIGHT[4], self.DOWN[4], self.LEFT[4] = self.RIGHT[4], self.DOWN[4], self.LEFT[4], self.UP[4]
                self.UP[5], self.RIGHT[7], self.DOWN[3], self.LEFT[1] = self.RIGHT[7], self.DOWN[3], self.LEFT[1], self.UP[5]
        else:
            if clockwise:
                self.FRONT[3], self.RIGHT[3], self.BACK[3], self.LEFT[3] = self.LEFT[3], self.FRONT[3], self.RIGHT[3], self.BACK[3]
                self.FRONT[4], self.RIGHT[4], self.BACK[4], self.LEFT[4] = self.LEFT[4], self.FRONT[4], self.RIGHT[4], self.BACK[4]
                self.FRONT[5], self.RIGHT[5], self.BACK[5], self.LEFT[5] = self.LEFT[5], self.FRONT[5], self.RIGHT[5], self.BACK[5]
            else:
                self.FRONT[3], self.RIGHT[3], self.BACK[3], self.LEFT[3] = self.RIGHT[3], self.BACK[3], self.LEFT[3], self.FRONT[3]
                self.FRONT[4], self.RIGHT[4], self.BACK[4], self.LEFT[4] = self.RIGHT[4], self.BACK[4], self.LEFT[4], self.FRONT[4]
                self.FRONT[5], self.RIGHT[5], self.BACK[5], self.LEFT[5] = self.RIGHT[5], self.BACK[5], self.LEFT[5], self.FRONT[5]

    def midTurn180(self, lay):
        if lay == "M":
            self.UP[4], self.DOWN[4] = self.DOWN[4], self.UP[4]
            self.UP[1], self.DOWN[1] = self.DOWN[1], self.UP[1]
            self.UP[7], self.DOWN[7] = self.DOWN[7], self.UP[7]
            self.FRONT[4], self.BACK[4] = self.BACK[4], self.FRONT[4]
            self.FRONT[1], self.BACK[7] = self.BACK[7], self.FRONT[1]
            self.FRONT[7], self.BACK[1] = self.BACK[1], self.FRONT[7]
        elif lay == "E":
            self.FRONT[4], self.BACK[4] = self.BACK[4], self.FRONT[4]
            self.FRONT[3], self.BACK[3] = self.BACK[3], self.FRONT[3]
            self.FRONT[5], self.BACK[5] = self.BACK[5], self.FRONT[5]
            self.LEFT[4], self.RIGHT[4] = self.RIGHT[4], self.LEFT[4]
            self.LEFT[3], self.RIGHT[3] = self.RIGHT[3], self.LEFT[3]
            self.LEFT[5], self.RIGHT[5] = self.RIGHT[5], self.LEFT[5]
        elif lay == "S":
            self.UP[4], self.DOWN[4] = self.DOWN[4], self.UP[4]
            self.UP[3], self.DOWN[5] = self.DOWN[5], self.UP[3]
            self.UP[5], self.DOWN[3] = self.DOWN[3], self.UP[5]
            self.LEFT[4], self.RIGHT[4] = self.RIGHT[4], self.LEFT[4]
            self.LEFT[1], self.RIGHT[7] = self.RIGHT[7], self.LEFT[1]
            self.LEFT[7], self.RIGHT[1] = self.RIGHT[1], self.LEFT[7]
        else:
            raise TypeError

    def turnAll90(self, dire, clockwise):
        if dire == "x":
            self.faceTurn90("R", clockwise)
            self.faceTurn90("L", not clockwise)
            self.midTurn90("M", not clockwise)
        elif dire == "y":
            self.faceTurn90("U", clockwise)
            self.faceTurn90("D", not clockwise)
            self.midTurn90("E", not clockwise)
        else:
            self.faceTurn90("F", clockwise)
            self.faceTurn90("B", not clockwise)
            self.midTurn90("S", clockwise)

    def turnAll180(self, dire):
        if dire == "x":
            self.faceTurn180("R")
            self.faceTurn180("L")
            self.midTurn180("M")
        elif dire == "y":
            self.faceTurn180("U")
            self.faceTurn180("D")
            self.midTurn180("E")
        else:
            self.faceTurn180("F")
            self.faceTurn180("B")
            self.midTurn180("S")

    def doubleTurn90(self, face, clockwise):
        if face == 'r':
            self.faceTurn90("R", clockwise)
            self.midTurn90("M", not clockwise)
        elif face == 'l':
            self.faceTurn90("L", clockwise)
            self.midTurn90("M", clockwise)
        if face == 'u':
            self.faceTurn90("U", clockwise)
            self.midTurn90("E", not clockwise)
        elif face == 'd':
            self.faceTurn90("D", clockwise)
            self.midTurn90("E", clockwise)
        elif face == 'b':
            self.faceTurn90("B", clockwise)
            self.midTurn90("S", not clockwise)
        elif face == 'f':
            self.faceTurn90("F", clockwise)
            self.midTurn90("S", clockwise)

    def doubleTurn180(self, face):
        self.faceTurn180(face.upper())
        if face in ['r', 'l']:
            self.midTurn180("M")
        elif face in ['f', 'b']:
            self.midTurn180("S")
        else:
            self.midTurn180("E")

    def turn(self, blocks, is90, clockwise=1):
        if blocks in self.faces:
            if is90:
                self.faceTurn90(blocks, clockwise)
            else:
                self.faceTurn180(blocks)
        elif blocks in self.middles:
            if is90:
                self.midTurn90(blocks, clockwise)
            else:
                self.midTurn180(blocks)
        elif blocks in self.alls:
            if is90:
                self.turnAll90(blocks, clockwise)
            else:
                self.turnAll180(blocks)
        elif blocks in self.towLayers:
            if is90:
                self.doubleTurn90(blocks, clockwise)
            else:
                self.doubleTurn180(blocks)
        else:
            raise TypeError

        self.flushcolors()
        
    def isSolved(self):
        if not self.isSame(self.UP.copy()): return False
        if not self.isSame(self.DOWN.copy()): return False
        if not self.isSame(self.LEFT.copy()): return False
        if not self.isSame(self.RIGHT.copy()): return False
        if not self.isSame(self.FRONT.copy()): return False
        if not self.isSame(self.BACK.copy()): return False
        return True
    
    def getSolution(self):
        return ko.solve(self.turnToStr())
    
    def turnToStr(self):
        s = ""
        for i in self.UP: s += i
        for i in self.RIGHT: s += i
        for i in self.FRONT: s += i
        for i in self.DOWN: s += i
        for i in self.LEFT: s += i
        for i in self.BACK: s += i
        print(s)
        return s

    def isSame(self, block):
        return block[0] == block[1] == block[2] == block[3] == block[4] == block[5] == block[6] == block[7] == block[8]

    def flushcolors(self):
        for i in range(9):
            self.displayblocks[i].color = self.COLORS[self.UP[i]]
        for i in range(9):
            self.displayblocks[i+9].color = self.COLORS[self.RIGHT[i]]
        for i in range(9):
            self.displayblocks[i+18].color = self.COLORS[self.FRONT[i]]

    def setcolor(self, string):
        self.UP = list(string[:9])
        self.RIGHT = list(string[9:18])
        self.FRONT = list(string[18:27])
        self.DOWN = list(string[27:36])
        self.LEFT = list(string[36:45])
        self.BACK = list(string[45:])
        self.flushcolors()

    def showAlg(self):
        self.xyzstd()
        alg = self.getSolution()
        if self.isSolved():
            showinfo(title="当前状态", message="当前已复原。")
        else:
            showinfo(title="当前状态", message="白顶绿前："+alg)

    def changeAsAlg(self, string):
        self.xyzstd()
        turns = string.split(" ")
        for turn in turns:
            if turn[-1] == "'":
                self.turn(turn[0], 1, 0)
            elif turn[-1] == "2":
                self.turn(turn[0], 0)
            else:
                self.turn(turn, 1)
        self.flushcolors()

    def autosolve(self):
        self.xyzstd()
        turns = self.getSolution().split(" ")
        if self.isSolved():
            showinfo(title="当前状态", message="当前已复原。")
        else:
            for turn in turns:
                time.sleep(0.02)
                if turn[-1] == "'":
                    self.turn(turn[0], 1, 0)
                elif turn[-1] == "2":
                    self.turn(turn[0], 0)
                else:
                    self.turn(turn, 1)
                self.flushcolors()

    def scramble(self):
        scramstr = ""
        a = ["R", "L", "U", "D", "F", "B"]
        r = ["L", "U", "D", "F", "B"]
        l = ["R", "U", "D", "F", "B"]
        u = ["R", "L", "D", "F", "B"]
        f = ["R", "L", "U", "D", "B"]
        b = ["R", "L", "U", "D", "F"]
        d = ["R", "L", "U", "F", "B"]
        buff = [" ", "' ", "2 "]
        self.allreset()
        cur = random.choice(a)
        scramstr+=cur
        scramstr+=random.choice(buff)
        for i in range(30):
            if cur == "R":
                cur = random.choice(r)
                scramstr+=cur
                scramstr+=random.choice(buff)
            elif cur == "L":
                cur = random.choice(l)
                scramstr+=cur
                scramstr+=random.choice(buff)
            elif cur == "U":
                cur = random.choice(u)
                scramstr+=cur
                scramstr+=random.choice(buff)
            elif cur == "D":
                cur = random.choice(d)
                scramstr+=cur
                scramstr+=random.choice(buff)
            elif cur == "F":
                cur = random.choice(f)
                scramstr+=cur
                scramstr+=random.choice(buff)
            elif cur == "B":
                cur = random.choice(b)
                scramstr+=cur
                scramstr+=random.choice(buff)
        scramstr = scramstr[:-1]
        print(scramstr)
        self.changeAsAlg(scramstr)

def sysQuit():
    pygame.display.quit()
    pygame.quit()
    sys.exit()

class CubeWindow:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(winSize)
        pygame.display.set_caption("魔方模拟")
        self.clock = pygame.time.Clock()

        while True:
            for event in pygame.event.get():
                if event == pygame.QUIT:
                    sysQuit()

            self.screen.fill(cube.COLORS["black"])
            # 27 blocks
            for block in cube.displayblocks:
                pygame.draw.polygon(self.screen, block.color, block.points, width = 0)
            for line in cube.lineps:
                pygame.draw.aaline(self.screen, (0, 0, 0), line[0], line[1], 1)

            pygame.display.flip()
            self.clock.tick(60)

class ControlWindow:
    def __init__(self, root):
        root.title("魔方模拟")
        root.resizable(0, 0)

        menubar = Menu(root)

        menubar.add_command(label="复原", command=cube.allreset)
        scramMenu = Menu(menubar, tearoff=False)
        scramMenu.add_command(label="随机打乱", command=cube.scramble)
        scramMenu.add_command(label="手动输入", command=self.insertStr)
        menubar.add_cascade(label="打乱", menu=scramMenu)
        solveMenu = Menu(menubar, tearoff=False)
        solveMenu.add_command(label="当前状态", command=cube.showAlg)
        solveMenu.add_command(label="自动还原", command=cube.autosolve)
        menubar.add_cascade(label="求解", menu=solveMenu)
        #menubar.add_command(label="设置", command=None)
        menubar.add_command(label="退出程序", command=sysQuit)

        root.config(menu=menubar)

        Button(root, text="M", font=("Consolas", 20), width=5, command=lambda:cube.turn("M", 1)).grid(row=0, column=0)
        Button(root, text="M'", font=("Consolas", 20), width=5, command=lambda:cube.turn("M", 1, 0)).grid(row=0, column=1)
        Button(root, text="M2", font=("Consolas", 20), width=5, command=lambda:cube.turn("M", 0)).grid(row=0, column=2)

        Button(root, text="S", font=("Consolas", 20), width=5, command=lambda:cube.turn("S", 1)).grid(row=1, column=0)
        Button(root, text="S'", font=("Consolas", 20), width=5, command=lambda:cube.turn("S", 1, 0)).grid(row=1, column=1)
        Button(root, text="S2", font=("Consolas", 20), width=5, command=lambda:cube.turn("S", 0)).grid(row=1, column=2)

        Button(root, text="E", font=("Consolas", 20), width=5, command=lambda:cube.turn("E", 1)).grid(row=2, column=0)
        Button(root, text="E'", font=("Consolas", 20), width=5, command=lambda:cube.turn("E", 1, 0)).grid(row=2, column=1)
        Button(root, text="E2", font=("Consolas", 20), width=5, command=lambda:cube.turn("E", 0)).grid(row=2, column=2)

        Button(root, text="l", font=("Consolas", 20), width=5, command=lambda:cube.turn("l", 1)).grid(row=0, column=3)
        Button(root, text="l'", font=("Consolas", 20), width=5, command=lambda:cube.turn("l", 1 ,0)).grid(row=0, column=4)
        Button(root, text="l2", font=("Consolas", 20), width=5, command=lambda:cube.turn("l", 0)).grid(row=0, column=5)

        Button(root, text="L", font=("Consolas", 20), width=5, command=lambda:cube.turn("L", 1)).grid(row=1, column=3)
        Button(root, text="L'", font=("Consolas", 20), width=5, command=lambda:cube.turn("L", 1, 0)).grid(row=1, column=4)
        Button(root, text="L2", font=("Consolas", 20), width=5, command=lambda:cube.turn("L", 0)).grid(row=1, column=5)

        Button(root, text="f", font=("Consolas", 20), width=5, command=lambda:cube.turn("f", 1)).grid(row=3, column=3)
        Button(root, text="f'", font=("Consolas", 20), width=5, command=lambda:cube.turn("f", 1 ,0)).grid(row=3, column=4)
        Button(root, text="f2", font=("Consolas", 20), width=5, command=lambda:cube.turn("f", 0)).grid(row=3, column=5)

        Button(root, text="F", font=("Consolas", 20), width=5, command=lambda:cube.turn("F", 1)).grid(row=2, column=3)
        Button(root, text="F'", font=("Consolas", 20), width=5, command=lambda:cube.turn("F", 1, 0)).grid(row=2, column=4)
        Button(root, text="F2", font=("Consolas", 20), width=5, command=lambda:cube.turn("F", 0)).grid(row=2, column=5)

        Button(root, text="u", font=("Consolas", 20), width=5, command=lambda:cube.turn("u", 1)).grid(row=0, column=6)
        Button(root, text="u'", font=("Consolas", 20), width=5, command=lambda:cube.turn("u", 1, 0)).grid(row=0, column=7)
        Button(root, text="u2", font=("Consolas", 20), width=5, command=lambda:cube.turn("u", 0)).grid(row=0, column=8)

        Button(root, text="U", font=("Consolas", 20), width=5, command=lambda:cube.turn("U", 1)).grid(row=1, column=6)
        Button(root, text="U'", font=("Consolas", 20), width=5, command=lambda:cube.turn("U", 1, 0)).grid(row=1, column=7)
        Button(root, text="U2", font=("Consolas", 20), width=5, command=lambda:cube.turn("U", 0)).grid(row=1, column=8)

        Button(root, text="D", font=("Consolas", 20), width=5, command=lambda:cube.turn("D", 1)).grid(row=2, column=6)
        Button(root, text="D'", font=("Consolas", 20), width=5, command=lambda:cube.turn("D", 1, 0)).grid(row=2, column=7)
        Button(root, text="D2", font=("Consolas", 20), width=5, command=lambda:cube.turn("D", 0)).grid(row=2, column=8)

        Button(root, text="d", font=("Consolas", 20), width=5, command=lambda:cube.turn('d', 1)).grid(row=3, column=6)
        Button(root, text="d'", font=("Consolas", 20), width=5, command=lambda:cube.turn('d', 1, 0)).grid(row=3, column=7)
        Button(root, text="d2", font=("Consolas", 20), width=5, command=lambda:cube.turn('d', 0)).grid(row=3, column=8)

        Button(root, text="R", font=("Consolas", 20), width=5, command=lambda:cube.turn("R", 1)).grid(row=1, column=9)
        Button(root, text="R'", font=("Consolas", 20), width=5, command=lambda:cube.turn("R", 1, 0)).grid(row=1, column=10)
        Button(root, text="R2", font=("Consolas", 20), width=5, command=lambda:cube.turn("R", 0)).grid(row=1, column=11)

        Button(root, text="r", font=("Consolas", 20), width=5, command=lambda:cube.turn('r', 1)).grid(row=0, column=9)
        Button(root, text="r'", font=("Consolas", 20), width=5, command=lambda:cube.turn('r', 1, 0)).grid(row=0, column=10)
        Button(root, text="r2", font=("Consolas", 20), width=5, command=lambda:cube.turn('r', 0)).grid(row=0, column=11)

        Button(root, text="B", font=("Consolas", 20), width=5, command=lambda:cube.turn("B", 1)).grid(row=2, column=9)
        Button(root, text="B'", font=("Consolas", 20), width=5, command=lambda:cube.turn("B", 1, 0)).grid(row=2, column=10)
        Button(root, text="B2", font=("Consolas", 20), width=5, command=lambda:cube.turn("B", 0)).grid(row=2, column=11)

        Button(root, text="b", font=("Consolas", 20), width=5, command=lambda:cube.turn('b', 1)).grid(row=3, column=9)
        Button(root, text="b'", font=("Consolas", 20), width=5, command=lambda:cube.turn('b', 1, 0)).grid(row=3, column=10)
        Button(root, text="b2", font=("Consolas", 20), width=5, command=lambda:cube.turn('b', 0)).grid(row=3, column=11)

        Button(root, text="x", font=("Consolas", 20), width=5, command=lambda:cube.turn('x', 1)).grid(row=0, column=12)
        Button(root, text="x'", font=("Consolas", 20), width=5, command=lambda:cube.turn('x', 1, 0)).grid(row=0, column=13)
        Button(root, text="x2", font=("Consolas", 20), width=5, command=lambda:cube.turn('x', 0)).grid(row=0, column=14)

        Button(root, text="y", font=("Consolas", 20), width=5, command=lambda:cube.turn('y', 1)).grid(row=1, column=12)
        Button(root, text="y'", font=("Consolas", 20), width=5, command=lambda:cube.turn('y', 1, 0)).grid(row=1, column=13)
        Button(root, text="y2", font=("Consolas", 20), width=5, command=lambda:cube.turn('y', 0)).grid(row=1, column=14)

        Button(root, text="z", font=("Consolas", 20), width=5, command=lambda:cube.turn('z', 1)).grid(row=2, column=12)
        Button(root, text="z'", font=("Consolas", 20), width=5, command=lambda:cube.turn('z', 1, 0)).grid(row=2, column=13)
        Button(root, text="z2", font=("Consolas", 20), width=5, command=lambda:cube.turn('z', 0)).grid(row=2, column=14)

        self.timer = Timer()

        stopButton = Button(root, textvariable=self.timer.buttontext, font=("Microsoft YaHei", 20), width=15, command=self.timer.control)
        stopButton.grid(row=3, column=0, columnspan=3)

        timeLabel = Label(root, textvariable=self.timer.timetext, font=("Microsoft YaHei", 20), width=15)
        timeLabel.grid(row=3, column=12, columnspan=3)

    def insertStr(self):
        self.top = Toplevel()
        self.top.title("魔方状态")
        self.top.resizable(0, 0)
        Message(self.top, text="""白顶绿前，按URFDLB的顺序，不留空格，其中复原状态为:
   UUU
   UUU
   UUU
LLLFFFRRRBBB
LLLFFFRRRBBB
LLLFFFRRRBBB
   DDD
   DDD
   DDD""", font=("MicroSoft YaHei", 15)).pack()
        self.en = Entry(self.top, width=60)
        self.en.pack()
        #self.en.insert(0, StateString.get())
        Button(self.top, text="导入", font=("MicroSoft YaHei", 15), command=self.getStr).pack()

    def getStr(self):
        #StateString.set(self.en.get())
        try:
            solution = ko.solve(self.en.get())
            cube.setcolor(self.en.get())
        except:
            showinfo(title="错误", message="输入不合法。")

class Timer:
    def __init__(self):
        self.buttontext = StringVar()
        self.buttontext.set("开始")
        self.timetext = StringVar()
        self.timetext.set("0.000")
        self.firstTime = 0
        self.secondTime = 0
        self.timerStart = Thread(target=self.start)
        self.running = False
        self.reseted = True
        
    def start(self):
        if cube.isSolved():
            showwarning(title="错误", message="魔方未打乱")
            self.timerStart = Thread(target=self.start)
            #print("Start1: running = %d" % self.running)
            return
        self.buttontext.set("停止")
        self.firstTime = time.time()
        self.running = True
        #print("Start2: running = %d" % self.running)
        while self.running:
            #print("Start Running: running = %d" % self.running) ##########
            self.secondTime = time.time()
            self.timetext.set("%.3f" % (self.secondTime-self.firstTime))
            time.sleep(0.01)
            if cube.isSolved():
                self.stop()
            # if self.running == False : break

    def stop(self):
        #print("Stop: running = %d" % self.running) ###########
        self.running = False
        self.reseted = False
        self.buttontext.set("清零")
        if cube.isSolved():
            self.timetext.set("%.3f" % (self.secondTime-self.firstTime))
        else:
            self.timetext.set("Did Not Finish")

    def reset(self):
        self.buttontext.set("开始")
        self.timetext.set("0.000")
        self.reseted = True
        self.timerStart = Thread(target=self.start)

    def control(self):
        if self.running:
            self.stop()
        else:
            if self.reseted:
                self.timerStart.start()
            else:
                self.reset()

winSize = width, height = 708, 647

cube = Cube()
root = Tk()
#StateString = StringVar()
#StateString.set("")

def showCubeWin():
    cube.turn("x", 0)
    global cuWin
    cuWin = CubeWindow()

graphThread = Thread(target=showCubeWin)

def main():
    global ctWin
    ctWin = ControlWindow(root)
    graphThread.start()
    root.mainloop()

if __name__ == "__main__":
    main()
