from numpy import *

def Rx(angle):  
    a = angle *pi/180
    return array([[1, 0, 0], [0, cos(a), -sin(a)], [0, sin(a), cos(a)]])

def Ry(angle):  
    a = angle *pi/180
    return array([[cos(a), 0, sin(a)], [0, 1, 0], [-sin(a), 0, cos(a)]])

def Rz(angle):  
    a = angle *pi/180
    return array([[cos(a), -sin(a), 0], [sin(a), cos(a), 0], [0, 0, 1]])


"""
A = array([[3, 6, 7], [5, -3, 0]])
B =  array([[1, 1], [2, 1], [3, -3]])
C = A.dot(B)
print(C)"""

print(arctan2(1,1))