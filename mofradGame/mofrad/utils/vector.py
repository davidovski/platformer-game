import math
def magnitude(v):
    return math.sqrt(v[0]*v[0] + v[1]*v[1])

def add(u, v):
    return [ u[i]+v[i] for i in range(len(u)) ]

def sub(u, v):
    return [ u[i]-v[i] for i in range(len(u)) ]

def dot(u, v):
    return sum(u[i]*v[i] for i in range(len(u)))

def normalize(v):
    vmag = magnitude(v)
    return [v[i]/vmag for i in range(len(v))]

class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def add(self, x, y):
        self.x += x
        self.y += y

    def add(self, vector):
        self.x += vector.x
        self.y += vector.y

    def sub(self, x, y):
        self.x -= x
        self.y -= y

    def sub(self, vector):
        self.x -= vector.x
        self.y -= vector.y

    def mul(self, x, y):
        self.x *= x
        self.y *= y

    def mul(self, ammount):
        self.x *= ammount
        self.y *= ammount

    def mul(self, vector):
        self.x *= vector.x
        self.y *= vector.y

    def mul(self, x, y):
        self.x *= x
        self.y *= y

    def set(self, x, y):
        self.x = x
        self.y = y
