import kociemba as ko
from tkinter import *

class ColorBlock:
    def __init__(self, color, pol, type):
        self.color = color
        if type == "F":
            self.points = [pol[0], pol[1],\
                           pol[0] + 99, pol[1] + 12,\
                           pol[0] + 99, pol[1] + 112,\
                           pol[0], pol[1] + 100]
        elif type == "U":
            self.points = [pol[0], pol[1],\
                           pol[0] + 99, pol[1] + 12,\
                           pol[0] + 62, pol[1] + 49,\
                           pol[0] - 37, pol[1] + 37]
        elif type == "R":
            self.points = [pol[0], pol[1],\
                           pol[0] + 37, pol[1] - 37,\
                           pol[0] + 37, pol[1] + 63,\
                           pol[0], pol[1] + 100]
        else:
            raise TypeError

class Cube:
    def __init__(self):
        """
        up = White, front = green, when program use scamble
        else, up = yellow, front = blue
        the string is made up with the chars from up, right, front, down, left, back
        """
        self.UP = ["U"] * 9
        self.RIGHT = ["R"] * 9
        self.FRONT = ["F"] * 9
        self.DOWN = ["D"] * 9
        self.LEFT = ["L"] * 9
        self.BACK = ["B"] * 9

        self.cx = 100
        self.cy = 100

        # default colors 白顶绿前
        self.u = "white"
        self.r = "red"
        self.f = "#2FC96C" # green
        self.l = "#FF8A00" # orange
        self.d = "#F2FF18" # yellow
        self.b = "#0873FF" # blue

        self.displaycolors = []
        self.displaypositions = [[[111, 0], [210, 12], [309, 24],\
                                  [74, 37], [173, 49], [272, 61],\
                                  [37, 74], [136, 86], [235, 98]],\
                                 [[297, 147], [334, 110], [371, 73],\
                                  [297, 247], [334, 210], [371, 173],\
                                  [297, 347], [334, 310], [371, 273]],\
                                 [[0, 111], [99, 123], [198, 135],\
                                  [0, 211], [99, 223], [198, 235],\
                                  [0, 311], [99, 323], [198, 335]]]
        for i in self.displaypositions:
            for j in i:
                j[0] += self.cx
                j[1] += self.cy

        for i in range(9):
            self.displaycolors.append(ColorBlock(self.u, self.displaypositions[0][i], "U"))
        for i in range(9):
            self.displaycolors.append(ColorBlock(self.r, self.displaypositions[1][i], "R"))
        for i in range(9):
            self.displaycolors.append(ColorBlock(self.f, self.displaypositions[2][i], "F"))

    def transcolor(self, char):
        if char == "U": return self.u
        elif char == "D": return self.d
        elif char == "R": return self.r
        elif char == "L": return self.l
        elif char == "F": return self.f
        elif char == "B": return self.b
        else: raise TypeError

    def reset(self):
        self.UP = ["U"] * 9
        self.RIGHT = ["R"] * 9
        self.FRONT = ["F"] * 9
        self.DOWN = ["D"] * 9
        self.LEFT = ["L"] * 9
        self.BACK = ["B"] * 9

    def turn90(self, dire, clockwise):
        # direction is like self.UP and so on
        # clockwise is True or False
        # R -> clockwise=T  R' -> clockwise=F
        if dire == self.UP:
            # 面上8格自旋转
            self.UP = self.UP[6::-3]+self.UP[7::-3]+self.UP[8::-3]\
                if clockwise else self.UP[2::3]+self.UP[1::3]+self.UP[::3]
            # 4个侧面涉及到的色块交换
            self.FRONT[:3], self.RIGHT[:3], self.BACK[:3], self.LEFT[:3]\
                = self.RIGHT[:3], self.BACK[:3], self.LEFT[:3], self.FRONT[:3] if clockwise else\
                self.LEFT[:3], self.FRONT[:3], self.RIGHT[:3], self.BACK[:3]
        elif dire == self.DOWN:
            self.DOWN = self.DOWN[6::-3]+self.DOWN[7::-3]+self.DOWN[8::-3]\
                if clockwise else self.DOWN[2::3]+self.DOWN[1::3]+self.DOWN[::3]
            self.FRONT[6:], self.RIGHT[6:], self.BACK[6:], self.LEFT[6:]\
                = self.LEFT[6:], self.FRONT[6:], self.RIGHT[6:], self.BACK[6:] if clockwise else\
                self.RIGHT[6:], self.BACK[6:], self.LEFT[6:], self.FRONT[6:]
        elif dire == self.RIGHT:
            self.RIGHT = self.RIGHT[6::-3]+self.RIGHT[7::-3]+self.RIGHT[8::-3]\
                if clockwise else self.RIGHT[2::3]+self.RIGHT[1::3]+self.RIGHT[::3]
            self.FRONT[2::3], self.DOWN[2::3], self.BACK[6::-3], self.UP[2::3]\
                = self.DOWN[2::3], self.BACK[6::-3], self.UP[2::3] if clockwise else\
                self.UP[2::3], self.FRONT[2::3], self.DOWN[2::3], self.BACK[6::-3]
        elif dire == self.LEFT:
            self.LEFT = self.LEFT[6::-3]+self.LEFT[7::-3]+self.LEFT[8::-3]\
                if clockwise else self.LEFT[2::3]+self.LEFT[1::3]+self.LEFT[::3]
            self.UP[::3], self.FRONT[::3], self.DOWN[::3], self.BACK[8::-3]\
                = self.BACK[8::-3], self.UP[::3], self.FRONT[::3], self.DOWN[::3] if clockwise else\
                self.FRONT[::3], self.DOWN[::3], self.BACK[8::-3], self.UP[::3]
        elif dire == self.FRONT:
            self.FRONT = self.FRONT[6::-3]+self.FRONT[7::-3]+self.FRONT[8::-3]\
                if clockwise else self.FRONT[2::3]+self.FRONT[1::3]+self.FRONT[::3]
            self.UP[6:], self.RIGHT[::3], self.DOWN[2::-1], self.LEFT[8::-3]\
                = self.LEFT[8::-3], self.UP[6:], self.RIGHT[::3], self.DOWN[2::-1] if clockwise else\
                self.RIGHT[::3], self.DOWN[2::-1], self.LEFT[8::-3], self.UP[6:]
        elif dire == self.BACK:
            self.BACK = self.BACK[6::-3]+self.BACK[7::-3]+self.BACK[8::-3]\
                if clockwise else self.BACK[2::3]+self.BACK[1::3]+self.BACK[::3]
            self.UP[:3], self.RIGHT[2::3], self.DOWN[8:5:-1], self.LEFT[6::-3]\
                = self.RIGHT[2::3], self.DOWN[8:5:-1], self.LEFT[6::-3], self.UP[:3] if clockwise else\
                self.LEFT[6::-3], self.UP[:3], self.RIGHT[2::3], self.DOWN[8:5:-1]
        else:
            raise TypeError("use error")
    
    def turn180(self, dire):
        dire[:4], dire[8:4:-1] = dire[8:4:-1], dire[:4]
        if dire == self.UP:
            self.FRONT[:3], self.BACK[:3] = self.BACK[:3], self.FRONT[:3]
            self.LEFT[:3], self.RIGHT[:3] = self.RIGHT[:3], self.LEFT[:3]
        elif dire == self.DOWN:
            self.FRONT[6:], self.BACK[6:] = self.BACK[6:], self.FRONT[6:]
            self.LEFT[6:], self.RIGHT[6:] = self.RIGHT[6:], self.LEFT[6:]
        elif dire == self.LEFT:
            self.UP[::3], self.DOWN[::3] = self.DOWN[::3], self.UP[::3]
            self.FRONT[::3], self.BACK[8:1:-3] = self.BACK[8:1:-3], self.FRONT[::3]
        elif dire == self.RIGHT:
            self.UP[2::3], self.DOWN[2::3] = self.DOWN[2::3], self.UP[2::3]
            self.FRONT[2::3], self.BACK[6::-3] = self.BACK[6::-3], self.FRONT[2::3]
        elif dire == self.FRONT:
            self.UP[6:], self.DOWN[2::-1] = self.DOWN[2::-1], self.UP[6:]
            self.RIGHT[::3], self.LEFT[8:1:-3] = self.LEFT[8:1:-3], self.RIGHT[::3]
        elif dire == self.BACK:
            self.UP[:3], self.DOWN[8:5:-1] = self.DOWN[8:5:-1], self.UP[:3]
            self.RIGHT[2::3], self.LEFT[::3] = self.LEFT[::3], self.RIGHT[2::3]
        else:
            raise ValueError("use error")
        
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
        pass

    def isSame(self, block):
        return block[0] == block[1] == block[2] == block[3] == block[4] == block[5] == block[6] == block[7] == block[8]

    def refresh(self):
        pass

class Window:
    def __init__(self, root):
        root.title("Cube Simulator")
        cubeCan = Canvas(root, bg="pink", height=700, width=900)
        self.blocks = []
        for item in cube.displaycolors:
            self.blocks.append(cubeCan.create_polygon(item.points, outline="black", fill=item.color, width=3))
        #for i in self.blocks:print(i)

        cubeCan.pack()

def main():
    global cube
    cube = Cube()
    global root
    root = Tk()
    theWindow = Window(root)
    root.mainloop()

if __name__ == "__main__":
    main()