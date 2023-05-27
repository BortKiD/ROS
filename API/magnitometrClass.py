import random
import time
import math

# Класс гироскопа
class Magnitometr():

    # Инициализируем гироскоп по переданному в конструктор регистру    
    def __init__(self, register:int):
        print('Магнитометр найден!')
        self.register = register
            
    # Устанавливаем частоту опроса гироскопа по переданному параметру
    # Возвращает Истину или Ложь, в зависимости корректно ли передан параметр частоты опроса
    def SetMeasurementRate(self, miliseconds:float) -> bool:
        if (miliseconds <= 0):
            print('Переданная частота должна быть положительной!')
            return False
        else:
            self.measurement_rate = miliseconds
        return True
    
    # В данном методе опрашиваем гироскоп, считая данные по 6 байт
    # На каждую ось приходится младший и старший байт, которые затем складываются
    # Возвращает массив значений по каждой оси в трехмерной системе координат
    def GetMeasurementData(self):
        # xMagn = random.uniform(-32768, 32768)
        # yMagn = random.uniform(-32768, 32768)
        # zMagn = random.uniform(-32768, 32768)
        xMagn = 30
        yMagn = 30
        zMagn = 30

        return [xMagn, yMagn, zMagn]

            
