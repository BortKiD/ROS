# Класс, хранящий значение зафиксированной  точки, её координаты (x, y),
# дистанцию от лидара до этой точки и угол под которым эта точка была получена 
from collections.abc import Iterator, Iterable

class Point():
    def __init__(self, x:int, y:int, length:float, angle:float):
        self.X = x
        self.Y = y
        self.Length = length
        self.Angle = angle

    def __str__(self) -> str:
        lst = [self.X, self.Y, self.Length, self.Angle]
        return str(lst)

    def __iter__(self) -> Iterable[int]:
        yield self.X
        yield self.Y
        yield self.Length
        yield self.Angle
    
