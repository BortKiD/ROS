import time
from datetime import datetime
from threading import Thread
from acclerometerClass import *
from gyroscopeClass import *
from magnitometrClass import *
from DatasetClass import *
from lidarClass import *
from PointClass import *
from dataHandler import *
from DataStorage import *

class Dispatcher():
    """Класс диспетчера, производящий создание и вызов считывания у объектов классов датчиков."""
    def __init__(self):
        self.Dataset = Dataset()
        self.AccelerometerFrequency = 1
        self.MagnitometerFrequency = 1
        self.GyroscopeFrequency = 1
        self.LidarFrequency = 1
        self.WriteFile = {
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
        #self.current_datetime = datetime.datetime(1,1,1)
        self.start_date = datetime.now().strftime("%Y-%m-%d")
        self.start_time = time.strftime("%H:%M:%S")


    def AddAccelerometer(self, register:int, rate:float):
        """Добавляет датчик акселлерометра в диспетчер."""
        accelerometer = Accelerometer(register)
        accelerometer.SetMeasurementRate(rate)
        self.AccelerometerFrequency = rate
        self.AcclMass.append(accelerometer)

    def AddGyro(self, register:int, rate:float):
        """Добавляет датчик гироскопа в диспетчер."""
        Gyro = Gyroscope(register)
        Gyro.SetMeasurementRate(rate)
        self.GyroscopeFrequency = rate
        self.GyroMass.append(Gyro)

    def AddMagnitometer(self, register:int, rate:float):
        """Добавляет датчик магнитометра в диспетчер."""
        magnitometer = Magnitometr(register)
        magnitometer.SetMeasurementRate(rate)
        self.MagnitometerFrequency = rate
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
        self.WriteFile[sensor] = value

    def StartThreads(self):
        def Accl(accl):
            data_storage = DataStorage()
            while True:
                if isSensorFrequencyChanged(accl, self.AccelerometerFrequency):
                    print("Accelerometer: frequency changed")
                    accl.SetMeasurementRate(self.AccelerometerFrequency)
                
                if self.AccelerometerFrequency:
                    time.sleep(1/accl.measurement_rate)
                    xAccl, yAccl, zAccl = accl.GetMeasurementData()
                    self.Dataset.xAccl, self.Dataset.yAccl, self.Dataset.zAccl = xAccl, yAccl, zAccl
                    roll = DataHandler.GetRoll(yAccl, zAccl)
                    pitch = DataHandler.GetPitch(xAccl, yAccl, zAccl)
                    # Save data format: [current_date, current_time, xAccl, yAccl, zAccl]
                    if self.WriteFile['accl']:
                        ctime = time.strftime("%H:%M:%S")
                        data_storage.save_data((ctime, xAccl, yAccl, zAccl))
                        filename = "accelerometer-" + str(self.start_date) + "-" + str(self.start_time) + ".csv"
                        data_storage.save_to_file(filename)
                    self.Dataset.Roll = roll
                    self.Dataset.Pitch = pitch
                else:
                    time.sleep(1)

        def Gyro(gyro):
            data_storage = DataStorage()
            while True:
                if isSensorFrequencyChanged(gyro, self.GyroscopeFrequency):
                    print("Gyroscope: frequency changed")
                    gyro.SetMeasurementRate(self.GyroscopeFrequency)
                
                if self.GyroscopeFrequency:
                    time.sleep(1/gyro.measurement_rate)
                    xGyro, yGyro, zGyro = gyro.GetMeasurementData()
                    # Save data format: [current_date, current_time, xGyro, yGyro, zGyro]
                    if self.WriteFile['gyro']:
                        ctime = time.strftime("%H:%M:%S")
                        data_storage.save_data((ctime, xGyro, yGyro, zGyro))
                        filename = "gyroscope-" + str(self.start_date) + "-" + str(self.start_time) + ".csv"
                        data_storage.save_to_file(filename)
                    self.Dataset.xGyro, self.Dataset.yGyro, self.Dataset.zGyro = xGyro, yGyro, zGyro
                else:
                    time.sleep(1)
                
        def Magn(magn):
            data_storage = DataStorage()
            while True:
                if isSensorFrequencyChanged(magn, self.MagnitometerFrequency):
                    print("Magnitometer: frequency have changed")
                    magn.SetMeasurementRate(self.MagnitometerFrequency)
                
                if self.MagnitometerFrequency:
                    time.sleep(1/magn.measurement_rate)
                    xMagn, yMagn, zMagn = magn.GetMeasurementData()
                    # Save data format: [current_date, current_time, xMagn, yMagn, zMagn]
                    if self.WriteFile['magn']:
                        ctime = time.strftime("%H:%M:%S")
                        data_storage.save_data((ctime, xMagn, yMagn, zMagn))
                        filename = "magnitometer-" + str(self.start_date) + "-" + str(self.start_time) + ".csv"
                        data_storage.save_to_file(filename)
                    self.Dataset.xMagn, self.Dataset.yMagn, self.Dataset.zMagn = xMagn, yMagn, zMagn
                    yaw = DataHandler.GetYaw(xMagn, yMagn)
                    yaw = DataHandler.TestYaw2(xMagn, yMagn, zMagn, self.Dataset.Roll, self.Dataset.Pitch)
                    self.Dataset.Yaw = yaw
                else:
                    time.sleep(1)

        def Lidar(lidar):
            data_storage = DataStorage(100)
            while True:
                if isSensorFrequencyChanged(lidar, self.LidarFrequency):
                    print("Lidar: frequency have changed")
                    lidar.SetMeasurementRate(self.LidarFrequency)
                
                if self.LidarFrequency:
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
                    if self.WriteFile['lidar']:
                        lst = []
                        for p in points_arr:
                            lst.append(p.getValues())
                        ctime = time.strftime("%H:%M:%S")
                        data_storage.save_data((ctime, lst))
                        filename = "lidar-" + str(self.start_date) + "-" + str(self.start_time) + ".csv"
                        data_storage.save_to_file(filename)
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
