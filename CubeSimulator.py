import kociemba as ko
from tkinter import *

class Cube:
    def __init__(self):
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

    def turn90(self, dire, prime):
        # direction is like self.UP and so on
        # prime is True or False
        if dire == self.UP:
            self.UP = self.UP[6::-3]+self.UP[7::-3]+self.UP[8::-3]\
                if prime else self.UP[2::3]+self.UP[1::3]+self.UP[::3]
            self.FRONT[:3], self.RIGHT[:3], self.BACK[:3], self.LEFT[:3]\
                = self.RIGHT[:3], self.BACK[:3], self.LEFT[:3], self.FRONT[:3] if prime else\
                self.LEFT[:3], self.FRONT[:3], self.RIGHT[:3], self.BACK[:3]
        elif dire == self.DOWN:
            self.DOWN = self.DOWN[6::-3]+self.DOWN[7::-3]+self.DOWN[8::-3]\
                if prime else self.DOWN[2::3]+self.DOWN[1::3]+self.DOWN[::3]
            self.FRONT[6:], self.RIGHT[6:], self.BACK[6:], self.LEFT[6:]\
                = self.LEFT[6:], self.FRONT[6:], self.RIGHT[6:], self.BACK[6:] if prime else\
                self.RIGHT[6:], self.BACK[6:], self.LEFT[6:], self.FRONT[6:]
        elif dire == self.RIGHT:
            self.RIGHT = self.RIGHT[6::-3]+self.RIGHT[7::-3]+self.RIGHT[8::-3]\
                if prime else self.RIGHT[2::3]+self.RIGHT[1::3]+self.RIGHT[::3]
        elif dire == self.LEFT:
            self.LEFT = self.LEFT[6::-3]+self.LEFT[7::-3]+self.LEFT[8::-3]\
                if prime else self.LEFT[2::3]+self.LEFT[1::3]+self.LEFT[::3]
        elif dire == self.FRONT:
            self.FRONT = self.FRONT[6::-3]+self.FRONT[7::-3]+self.FRONT[8::-3]\
                if prime else self.FRONT[2::3]+self.FRONT[1::3]+self.FRONT[::3]
        elif dire == self.BACK:
            self.BACK = self.BACK[6::-3]+self.BACK[7::-3]+self.BACK[8::-3]\
                if prime else self.BACK[2::3]+self.BACK[1::3]+self.BACK[::3]
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

root = Tk()
root.title("Cube Simulator")



mainloop()
