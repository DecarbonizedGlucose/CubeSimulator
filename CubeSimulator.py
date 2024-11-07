import kociemba as ko
from tkinter import *

def isSame(block):
    pass

class Cube:
    def __init__(self):
        """
        up = White, front = green, when program use scamble
        else, up = yellow, front = blue
        """
        self.UP = ["U"] * 9
        self.RIGHT = ["R"] * 9
        self.FRONT = ["F"] * 9
        self.DOWN = ["D"] * 9
        self.LEFT = ["L"] * 9
        self.BACK = ["B"] * 9

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
        if not isSame(self.UP.copy()): return False
        if not isSame(self.DOWN.copy()): return False
        if not isSame(self.LEFT.copy()): return False
        if not isSame(self.RIGHT.copy()): return False
        if not isSame(self.FRONT.copy()): return False
        if not isSame(self.BACK.copy()): return False
        return True
    
    def getSolution(self):
        pass

root = Tk()
root.title("Cube Simulator")



mainloop()
