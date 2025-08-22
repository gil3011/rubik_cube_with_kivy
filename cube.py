import numpy as np
import random
class Cube:
    def __init__(self):
        colors = {
            "up": 'w', "front": 'r', "right": 'b',
            "left": 'g', "back": 'o', "down": 'y'
        }
        self.faces = {face: [[color]*3 for _ in range(3)] for face, color in colors.items()}
    def rotate_x(self,count = 1):
        for _ in range(count):
            self.m()
            self.r(3)
            self.l()
    def rotate_z(self, count = 1):
        for _ in range(count):
            self.s()
            self.f()
            self.b(3)        
    def rotate_y(self, count = 1):
        for _ in range(count):
            self.e()
            self.u(3)
            self.d()
    def u(self, count = 1):
        for _ in range(count):
            for i in range(3): 
                temp = self.faces['front'][0][i]
                self.faces['front'][0][i] = self.faces['right'][0][i]
                self.faces['right'][0][i] = self.faces['back'][0][i]
                self.faces['back'][0][i] = self.faces['left'][0][i]
                self.faces['left'][0][i] = temp
            self.faces['up'] = np.rot90(self.faces['up'],-1)
    def r(self, count = 1):
        for _ in range(count):
            for i in range(3):
                temp = self.faces['front'][i][2]
                self.faces['front'][i][2] = self.faces['down'][i][2]
                self.faces['down'][i][2] = self.faces['back'][2 - i][0]  # reversed because back is opposite
                self.faces['back'][2 - i][0] = self.faces['up'][i][2]
                self.faces['up'][i][2] = temp
            self.faces['right'] = np.rot90(self.faces['right'], -1)
    def f(self, count = 1):
        for _ in range(count):
            for i in range(3):
                temp = self.faces['up'][2][i]
                self.faces['up'][2][i] = self.faces['left'][2-i][2]
                self.faces['left'][2-i][2] = self.faces['down'][0][2-i]
                self.faces['down'][0][2-i] = self.faces['right'][i][0]
                self.faces['right'][i][0] = temp
            self.faces['front'] = np.rot90(self.faces['front'], -1)
    def l(self, count = 1):
        for _ in range (count):
            for i in range(3):
                temp = self.faces['front'][i][0]
                self.faces['front'][i][0] = self.faces['up'][i][0]
                self.faces['up'][i][0] = self.faces['back'][2 - i][2]  
                self.faces['back'][2 - i][2] = self.faces['down'][i][0]
                self.faces['down'][i][0] = temp
            self.faces['left'] = np.rot90(self.faces['left'], -1)
    def d(self, count = 1):
        for _ in range (count):
            for i in range(3):
                temp = self.faces['front'][2][i]
                self.faces['front'][2][i] = self.faces['left'][2][i]
                self.faces['left'][2][i] = self.faces['back'][2][i]
                self.faces['back'][2][i] = self.faces['right'][2][i]
                self.faces['right'][2][i] = temp
            self.faces['down'] = np.rot90(self.faces['down'],-1)
    def b(self, count = 1):
        for _ in range (count):
            for i in range(3):
                temp = self.faces['up'][0][i]
                self.faces['up'][0][i] = self.faces['right'][i][2]
                self.faces['right'][i][2] = self.faces['down'][2][2 - i]
                self.faces['down'][2][2 - i] = self.faces['left'][2 - i][0]
                self.faces['left'][2 - i][0] = temp
            self.faces['back'] = np.rot90(self.faces['back'], -1)
    def m(self):
        for i in range(3):
            temp = self.faces['front'][i][1]
            self.faces['front'][i][1] = self.faces['up'][i][1]
            self.faces['up'][i][1] = self.faces['back'][2-i][1]
            self.faces['back'][2-i][1] = self.faces['down'][i][1]
            self.faces['down'][i][1] = temp
    def s(self):
        for i in range (3):
            temp = self.faces['up'][1][i]
            self.faces['up'][1][i] = self.faces['left'][2-i][1] 
            self.faces['left'][2-i][1] = self.faces['down'][1][2-i] 
            self.faces['down'][1][2-i] = self.faces['right'][i][1]
            self.faces['right'][i][1] = temp
    def e(self):
        for i in range (3):
            temp = self.faces['front'][1][i]
            self.faces['front'][1][i] = self.faces['left'][1][i] 
            self.faces['left'][1][i] = self.faces['back'][1][i] 
            self.faces['back'][1][i] = self.faces['right'][1][i]
            self.faces['right'][1][i] = temp
    def shuffle(self):
        actions = [self.u, self.r, self.f, self.l, self.d,self.b]
        for _ in range(random.randint(20,45)):
            random.choice(actions)() 
    def is_solved(self):
        for face in self.faces.keys():
            color = self.faces[face][1][1]
            for i in range(3):
                for j in range(3):
                    if self.faces[face][i][j] != color:
                        return False
        return True
