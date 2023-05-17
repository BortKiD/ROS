# from PointClass import Point
# Класс для хранения данных с датчиков
class Dataset():
    def __init__(self):
        self.Points = []
        # Angle
        self.Roll = 0
        self.Pitch = 0
        self.Yaw = 0
        # Accelerometer
        self.xAccl = 0
        self.yAccl = 0
        self.zAccl = 0
        # Magnitometer
        self.xMagn = 0
        self.yMagn = 0
        self.zMagn = 0
        # Gyroscope
        self.xGyro = 0
        self.yGyro = 0
        self.zGyro = 0