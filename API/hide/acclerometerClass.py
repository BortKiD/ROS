from smbus import SMBus
import time
import math

# Класс акселерометра
class Accelerometer():

    ACCL_ZERO_REGISTER = 0x00 # Нулевой регистр
    ACCL_DEVICE_ID     = 0xe5 # ID устройства
    ACCL_PWR_REGISTER  = 0x2d # Регистр управления питанием
    
    ACCL_X_OFFSET      = 0x1e # Регистр, хранящий смещение значения по оси X
    ACCL_Y_OFFSET      = 0x1f # Регистр, хранящий смещение значения по оси Y
    ACCL_Z_OFFSET      = 0x20 # Регистр, хранящий смещение значения по оси Z
    
    ACCL_X_DATA0       = 0x32 # Регистр, хранящий главный байт данных по оси X
    ACCL_X_DATA1       = 0x33 # Регистр, хранящий младший байт данных по оси X
    ACCL_Y_DATA0       = 0x34 # Регистр, хранящий главный байт данных по оси Y
    ACCL_Y_DATA1       = 0x35 # Регистр, хранящий младший байт данных по оси Y
    ACCL_Z_DATA0       = 0x36 # Регистр, хранящий главный байт данных по оси Z
    ACCL_Z_DATA1       = 0x37 # Регистр, хранящий младший байт данных по оси Z
    
    # Инициализируем акселерометр по переданному в конструктор регистру
    def __init__(self, register:int):
        bus = SMBus(1)
        try:
            bus.read_byte_data(register, self.ACCL_ZERO_REGISTER)
        except ValueError:
            print('Устройство по регистру ' + str(register) + ' отсутствует!')
        if (bus.read_byte_data(register, self.ACCL_ZERO_REGISTER) == self.ACCL_DEVICE_ID):
            print('Акселерометр найден!')
            bus.write_byte_data(register, self.ACCL_PWR_REGISTER, 0x08)
            self.register = register
            self.Calibrate()
        else:
            print('Устройство по регистру ' + str(register) + ' не является аклселерометром!')            
    # Устанавливаем частоту опроса акселерометра по переданному параметру
    # Возвращает Истину или Ложь, в зависимости корректно ли передан параметр частоты опроса
    def SetMeasurementRate(self, miliseconds:float) -> bool:
        if (miliseconds <= 0):
            print('Переданная частота должна быть положительной!')
            return False
        else:
            self.measurement_rate = miliseconds
        return True
    # Метод для калибровки акселерометра.
    # Калибруем, путем записи значения -0x01 в регистры смещения по осям
    def Calibrate(self):
        bus = SMBus(1)
        bus.write_byte_data(self.register, self.ACCL_X_OFFSET, -0x01)
        bus.write_byte_data(self.register, self.ACCL_Y_OFFSET, -0x01)
        bus.write_byte_data(self.register, self.ACCL_Z_OFFSET, -0x01)
        
    # В данном методе опрашиваем акселерометр, считывая данные по 6 байт
    # На каждую ось приходится младший и старший байт, которые затем складываются
    # Возвращает массив значений по каждой оси в трехмерной системе координат
    def GetMeasurementData(self):
        bus = SMBus(1)
        data = bus.read_i2c_block_data(self.register, self.ACCL_X_DATA0, 6)

        xAccl = (data[1] & 0x03) * 256 + data[0]
        if xAccl > 511 :
            xAccl -= 1024

        yAccl = (data[3] & 0x03) *  256 + data[2]
        if yAccl > 511 :
            yAccl -= 1024

        zAccl = (data[5] & 0x03) * 256 + data[4]
        if zAccl > 511 :
            zAccl -= 1024

        return [xAccl, yAccl, zAccl]

