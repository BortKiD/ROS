from smbus import SMBus
import time
import math

# Класс магнитометра
class Magnitometr():
    #Документация находится здесь: https://cdn-shop.adafruit.com/datasheets/HMC5883L_3-Axis_Digital_Compass_IC.pdf
    MAGN_DEVICE_ID          = 0x1e # Регистр устройства на шине i2c
    MAGN_REGISTER_CRA       = 0x01 # Конфигурационный регистр
    MAGN_MEASUREMENT_MODE   = 0x00 # Регистр непрерывного измерения 
    MAGN_REGISTER_MODE      = 0x02 # Регистр отвечающий за режим измерения
    MAGN_MEASUREMENT_NORMAL = 0x00 # Регистр нормального измерен
    MAGN_X_DATA0            = 0x03 # Верхний регистр данных по X
    
    # Инициализируем магнитометр по переданному в конструктор регистру    
    def __init__(self, register:int):
        bus = SMBus(1)
        try:
            bus.read_byte_data(register, 0x00)
        except ValueError:
            print('Устройство по регистру ' + str(register) + ' отсутствует!')
        if (register == self.MAGN_DEVICE_ID):
            print('Магнитометр найден!')
            self.register = register
            bus.write_byte_data(self.register, self.MAGN_REGISTER_CRA, self.MAGN_MEASUREMENT_NORMAL)
            bus.write_byte_data(self.register, self.MAGN_REGISTER_MODE, self.MAGN_MEASUREMENT_MODE)
        else:
            print('Устройство по регистру ' + str(register) + ' не является магнитометр!')            
    # Устанавливаем частоту опроса магнитометра по переданному параметру
    # Возвращает Истину или Ложь, в зависимости корректно ли передан параметр частоты опроса
    def SetMeasurementRate(self, miliseconds:float) -> bool:
        if (miliseconds <= 0):
            print('Переданная частота должна быть положительной!')
            return False
        else:
            self.measurement_rate = miliseconds
        return True
    # В данном методе опрашиваем магнитометр, считая данные по 6 байт
    # На каждую ось приходится младший и старший байт, которые затем складываются
    # Возвращает массив значений по каждой оси в трехмерной системе координат
    def GetMeasurementData(self):
        bus = SMBus(1)
        data = bus.read_i2c_block_data(self.register, self.MAGN_X_DATA0, 6)

        xMag = data[0] * 256 + data[1]
        if xMag > 32767 :
            xMag -= 65536

        zMag = data[2] * 256 + data[3]
        if zMag > 32767 :
            zMag -= 65536

        yMag = data[4] * 256 + data[5]
        if yMag > 32767 :
            yMag -= 65536

        return [xMag, yMag, zMag]

