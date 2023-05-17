import math

#Класс, содержащий методы работы с данными
class DataHandler():

    #Метод получения крена.
    @staticmethod
    def GetRoll(yAccl:int, zAccl:int):
        try:
            return math.atan(yAccl / zAccl) * 180 / math.pi
        except ArithmeticError:
            print("Arithmetic error")

    #Метод получения тангажа.
    @staticmethod
    def GetPitch(xAccl:int, yAccl:int, zAccl:int):
        try:
            return math.atan(-1 * xAccl / math.sqrt(pow(yAccl,2) + math.pow(zAccl, 2))) * 180 / math.pi
        except ArithmeticError:
            print("Arithmetic error")

    #Метод получения рыскания.
    @staticmethod
    def GetYaw(xMagn:int, yMagn:int):
        try:
            return math.atan2(xMagn, yMagn) * 180 / math.pi
        except ArithmeticError:
            print("Arithmetic error")

    #Метод преобразования пары [угол, расстояние] в [x, y]
    @staticmethod
    def GetCoordinates(distance:float, angle:float):
        try:
            rad=math.radians(angle)            
            x=(distance * math.cos(rad))
            y=(distance * math.sin(rad))
            return [x, y]
        except ArithmeticError:
            print("Arithmetic error")

    @staticmethod
    def TestYaw(xAccl, yAccl, zAccl, xMang, yMagn):
        phi = DataHandler.GetRoll(yAccl, zAccl)
        theta = DataHandler.GetPitch(xAccl, yAccl, zAccl)
        By2 = zAccl * math.sin(phi) - yAccl * math.cos(phi)
        Bz2 = yAccl * math.sin(phi) + zAccl * math.cos(phi)
        Bx3 = xAccl * math.cos(theta) + Bz2 * math.sin(theta)
        return math.atan2(By2, Bx3)

    @staticmethod
    def TestYaw2(mx, my, mz, a_roll, a_pitch):
        Mx = mx * math.cos(a_pitch) + mz * math.sin(a_pitch)
        My = mx * math.sin(a_roll) * math.sin(a_pitch) + my * math.cos(a_roll) - mz * math.sin(a_roll) * math.cos(a_pitch)
        return math.atan(My / Mx) * 180 / math.pi
        return math.atan(mx/my) * 180 / math.pi
        
        
