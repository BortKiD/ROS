import time
import datetime
from threading import Thread
# from smbus import SMBus
from API.acclerometerClass import *
from API.gyroscopeClass import *
from API.magnitometrClass import *
from API.DatasetClass import *
from API.lidarClass import *
from API.PointClass import *
from API.dataHandler import *
from API.DataStorage import *

class Dispatcher():
    """Класс диспетчера, производящий создание и вызов считывания у объектов классов датчиков."""
    def __init__(self):
        self.Dataset = Dataset()
        self.AcclFreq = 1
        self.MagnFreq = 1
        self.GyroFreq = 1
        self.LidarFreq = 1
        self.writeFile = {
            "lidar":0,
            "accl":0,
            "magn":0,
            "gyro":0
        }
        self.AcclMass = []
        self.GyroMass = []
        self.MagnMass = []
        self.LidarMass = []
        self.SensorMass = [
            ("Accelerometer_pin", '53'),
            ("Magnitometer_pin", '1e'),
            ("Gyroscope_pin", '68'),
            ("Lidar_usb", '15d1:0000')]
        self.current_datetime = datetime.datetime(1,1,1)
        
    def AddAccelerometer(self, register:int, rate:float):
        """Добавляет датчик акселлерометра в диспетчер."""
        accelerometer = Accelerometer(register)
        accelerometer.SetMeasurementRate(rate)
        self.AcclFreq = rate
        self.AcclMass.append(accelerometer)

    def AddGyro(self, register:int, rate:float):
        """Добавляет датчик гироскопа в диспетчер."""
        Gyro = Gyroscope(register)
        Gyro.SetMeasurementRate(rate)
        self.GyroFreq = rate
        self.GyroMass.append(Gyro)

    def AddMagnitometer(self, register:int, rate:float):
        """Добавляет датчик магнитометра в диспетчер."""
        magnitometer = Magnitometr(register)
        magnitometer.SetMeasurementRate(rate)
        self.MagnFreq = rate
        self.MagnMass.append(magnitometer)

    def AddLidar(self, port:str, speed:int, rate:float):
        """Добавляет датчик лидара в диспетчер"""
        lidar = Lidar(port, speed)
        lidar.SetMeasurementRate(rate)
        self.LidarMass.append(lidar)

    def GetDataset(self):
        """Возвращает набор данных."""
        return self.Dataset
    
    def SetWritingFile(self, sensor, value):
        """Выставляет значение переменной включения/выключения записи файла."""
        self.writeFile[sensor] = value

    def StartThreads(self):
        def Accl(accl):
            data_storage = DataStorage()
            while True:
                if isSensorFrequencyChanged(accl, self.AcclFreq):
                    print("Accelerometer: frequency changed")
                    accl.SetMeasurementRate(self.AcclFreq)
                
                if self.AcclFreq:
                    time.sleep(1/accl.measurement_rate)
                    xAccl, yAccl, zAccl = accl.GetMeasurementData()
                    self.Dataset.xAccl, self.Dataset.yAccl, self.Dataset.zAccl = xAccl, yAccl, zAccl
                    roll = DataHandler.GetRoll(yAccl, zAccl)
                    pitch = DataHandler.GetPitch(xAccl, yAccl, zAccl)
                    # Save data format: [current_date, current_time, xAccl, yAccl, zAccl]
                    if self.writeFile['accl']:
                        date, ctime = self.current_datetime.now().isoformat().split("T")
                        data_storage.save_data((date, ctime, xAccl, yAccl, zAccl))
                        data_storage.save_to_file("accelerometer.csv")
                    self.Dataset.Roll = roll
                    self.Dataset.Pitch = pitch
                else:
                    time.sleep(1)

        def Gyro(gyro):
            data_storage = DataStorage()
            while True:
                if isSensorFrequencyChanged(gyro, self.GyroFreq):
                    print("Gyroscope: frequency changed")
                    gyro.SetMeasurementRate(self.GyroFreq)
                
                if self.GyroFreq:
                    time.sleep(1/gyro.measurement_rate)
                    xGyro, yGyro, zGyro = gyro.GetMeasurementData()
                    # Save data format: [current_date, current_time, xGyro, yGyro, zGyro]
                    if self.writeFile['gyro']:
                        date, ctime = self.current_datetime.now().isoformat().split("T")
                        data_storage.save_data((date, ctime, xGyro, yGyro, zGyro))
                        data_storage.save_to_file("gyroscope.csv")
                    self.Dataset.xGyro, self.Dataset.yGyro, self.Dataset.zGyro = xGyro, yGyro, zGyro
                else:
                    time.sleep(1)
                
        def Magn(magn):
            data_storage = DataStorage()
            while True:
                if isSensorFrequencyChanged(magn, self.MagnFreq):
                    print("Magnitometer: frequency have changed")
                    magn.SetMeasurementRate(self.MagnFreq)
                
                if self.MagnFreq:
                    time.sleep(1/magn.measurement_rate)
                    xMagn, yMagn, zMagn = magn.GetMeasurementData()
                    # Save data format: [current_date, current_time, xMagn, yMagn, zMagn]
                    if self.writeFile['magn']:
                        date, ctime = self.current_datetime.now().isoformat().split("T")
                        data_storage.save_data((date, ctime, xMagn, yMagn, zMagn))
                        data_storage.save_to_file("magnitometer.csv")
                    self.Dataset.xMagn, self.Dataset.yMagn, self.Dataset.zMagn = xMagn, yMagn, zMagn
                    yaw = DataHandler.GetYaw(xMagn, yMagn)
                    yaw = DataHandler.TestYaw2(xMagn, yMagn, zMagn, self.Dataset.Roll, self.Dataset.Pitch)
                    self.Dataset.Yaw = yaw
                else:
                    time.sleep(1)

        def Lidar(lidar):
            data_storage = DataStorage(100)
            while True:
                if isSensorFrequencyChanged(lidar, self.LidarFreq):
                    print("Lidar: frequency have changed")
                    lidar.SetMeasurementRate(self.LidarFreq)
                
                if not self.LidarFreq == 0:
                    time.sleep(1/lidar.measurement_rate)
                    lidar_arr = lidar.GetMeasurementData()
                    points_arr = []
                    for i in lidar_arr:
                        angle = i[0]
                        distance = i[1]
                        x, y = DataHandler.GetCoordinates(distance, angle)
                        point = Point(x, y, distance, angle)
                        points_arr.append(point)
                    # Save data format: [current_date, current_time, points]
                    if self.writeFile['lidar']:    
                        date, ctime = self.current_datetime.now().isoformat().split("T")
                        data_storage.save_data((date, ctime, points_arr))
                        data_storage.save_to_file("lidar.csv")
                    
                    self.Dataset.Points = points_arr
                else:
                    time.sleep(1)

        def isSensorFrequencyChanged(sensor, frequency):
            return not sensor.measurement_rate == frequency and not frequency == 0
        
        self.Threads = []
        for i in self.AcclMass:
            thread = Thread(target = Accl, args=(i,), daemon=True) 
            self.Threads.append(thread)
        self.AcclMass = []
        for i in self.GyroMass:
            thread = Thread(target = Gyro, args=(i,), daemon=True)
            self.Threads.append(thread)
        self.GyroMass = []
        for i in self.MagnMass:
            thread = Thread(target = Magn, args=(i,), daemon=True)
            self.Threads.append(thread)
        self.MagnMass = []
        for i in self.LidarMass:
            thread = Thread(target = Lidar, args=(i,), daemon=True)
            self.Threads.append(thread)
        self.LidarMass = []

        for i in self.Threads:
            i.start()
