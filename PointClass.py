# Класс, хранящий значение зафиксированной  точки, её координаты (x, y),
# дистанцию от лидара до этой точки и угол под которым эта точка была получена 
from collections.abc import Iterator, Iterable

class Point():
    def __init__(self, x:int, y:int, length:float, angle:float):
        self.X = x
        self.Y = y
        self.Length = length
        self.Angle = angle
    
