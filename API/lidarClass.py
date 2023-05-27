'''
Description: class, based on librarry hokuyo-python-lib
Author: paoole
Github: https://github.com/pasuder/hokuyo-python-lib
'''
import random

#Класс лидара.
class Lidar():

    #Конструктор, принимающий порт устройства, скорость считывания.
    def __init__(self, uart_port:str, uart_speed:int):
        try:
            port = uart_port
            speed = uart_speed
        except ValueError:
            print("Неверный порт!")

    #Метод, устанавливающий частоту считывания датчика в поле класса.
    def SetMeasurementRate(self, miliseconds:float) -> bool:
        if (miliseconds <= 0):
            print('Переданная частота должна быть положительной!')
            return False
        else:
            self.measurement_rate = miliseconds
        return True

    #Метод, производящий считывание точек.
    #Возвращает массив вида [[angle, distance],..], где angle - угол, distance - расстояние до точки.
    def GetMeasurementData(self):
        list=[]
        try:
            mass = []
            for i in range(-180, -50):
                # mass.append([i, round(random.uniform(10,15))])
                mass.append([i, 50])
            for i in range(-50, 50):
                # mass.append([i, round(random.uniform(10,15))])
                mass.append([i, 70])
            for i in range(60, 180):
                # mass.append([i, round(random.uniform(10,15))])
                mass.append([i, 90])

        except SystemError:
            print("Невозможно считать данные с лидара!")
        for key in mass:
            if key[0] > 60 or key[0] < -60:
                continue
            #Отсев "нулевых" точек
            if key[1] <= 10:
                continue
            list.append([key[0], key[1]])
        return list 
