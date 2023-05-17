import serial
import math
from hokuyo.driver import hokuyo
from hokuyo.tools import serial_port

'''
Description: class, based on librarry hokuyo-python-lib
Author: paoole
Github: https://github.com/pasuder/hokuyo-python-lib
'''

#Класс лидара.
class Lidar():

    #Конструктор, принимающий порт устройства, скорость считывания.
    def __init__(self, uart_port:str, uart_speed:int):
        try:
            laser_serial = serial.Serial(port=uart_port, baudrate=uart_speed, timeout=0.5)
            port = serial_port.SerialPort(laser_serial)
        except ValueError:
            print("Неверный порт!")
        self.laser = hokuyo.Hokuyo(port)        
        self.laser.laser_on()

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
            mass = self.laser.get_single_scan()
        except SystemError:
            print("Невозможно считать данные с лидара!")
        for key in mass.items():
            if key[0] > 60 or key[0] < -60:
                continue
            #if key[1] > 1500:
            #    continue
            #Отсев "нулевых" точек
            if key[1] <= 10:
                continue
            list.append([key[0], key[1]])
        return list 
