from numpy import *
PI = pi

def Rx(angle):
    a = angle * PI/180 
    b= array([[1, 0, 0], [0, cos(a), -1*sin(a)],[0, sin(a), cos(a)]])
    print(b)
    return b

print(Rx(30)[1][2])