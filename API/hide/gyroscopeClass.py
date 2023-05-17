from smbus import SMBus
import time
import math

# Класс гироскопа
class Gyroscope():

    # Документация гироскопа: https://goo.su/DcBSCh
    GYRO_DEVICE_ID     = 0x68 # Идентификатор
    GYRO_ZERO_REGISTER = 0x00 # Нулевой регистер
    GYRO_PWR_REGISTER  = 0x3e # Регистр управления питания
    GYRO_DLPF_REGISTER = 0x16 # Регистр настройки сбора данных 
    GYRO_X_DATA0       = 0x1d # Верхний регистр данных по Х
    
    # Инициализируем гироскоп по переданному в конструктор регистру    
    def __init__(self, register:int):
        bus = SMBus(1)
        try:
            bus.read_byte_data(register, self.GYRO_ZERO_REGISTER)
        except ValueError:
            print('Устройство по регистру ' + str(register) + ' отсутствует!')
        if (bus.read_byte_data(register, self.GYRO_ZERO_REGISTER) == register):
            print('Гироскоп найден!')
            self.register = register
            bus.write_byte_data(register, self.GYRO_PWR_REGISTER, 0x00)
            bus.write_byte_data(register, self.GYRO_DLPF_REGISTER, 0x18)
        else:
            print('Устройство по регистру ' + str(register) + ' не является гироскопом!')
            
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
        bus = SMBus(1)
        data = bus.read_i2c_block_data(self.register, self.GYRO_X_DATA0, 6)
        
        xGyro = data[0] * 256 + data[1]
        if xGyro > 32767 :
                xGyro -= 65536

        yGyro = data[2] * 256 + data[3]
        if yGyro > 32767 :
                yGyro -= 65536

        zGyro = data[4] * 256 + data[5]
        if zGyro > 32767 :
                zGyro -= 65536

        return [xGyro, yGyro, zGyro]

            
