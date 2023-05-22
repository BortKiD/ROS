from tkinter import *
from dispatcher import *

def update():
    xAccl, yAccl, zAccl = dispatcher.Dataset.xAccl, dispatcher.Dataset.yAccl, dispatcher.Dataset.zAccl
    label_xAccl['text'] = 'xAccl = ' + "{:.2f}".format(xAccl)
    label_yAccl['text'] = 'yAccl = ' + "{:.2f}".format(yAccl)
    label_zAccl['text'] = 'zAccl = ' + "{:.2f}".format(zAccl)
    
    xMagn, yMagn, zMagn = dispatcher.Dataset.Pitch, dispatcher.Dataset.Roll, dispatcher.Dataset.Yaw
    label_xMagn['text'] = 'xMagn = ' + "{:.2f}".format(xMagn)
    label_yMagn['text'] = 'yMagn = ' + "{:.2f}".format(yMagn)
    label_zMagn['text'] = 'zMagn = ' + "{:.2f}".format(zMagn)

    xGyro, yGyro, zGyro = dispatcher.Dataset.Pitch, dispatcher.Dataset.Roll, dispatcher.Dataset.Yaw
    label_xGyro['text'] = 'xGyro = ' + "{:.2f}".format(xGyro)
    label_yGyro['text'] = 'yGyro = ' + "{:.2f}".format(yGyro)
    label_zGyro['text'] = 'zGyro = ' + "{:.2f}".format(zGyro)

    root.after(100, update)

def set_freq(e):
    frequency = accelerometer_scale.get()
    dispatcher.AcclMass[0].SetMeasurementRate(frequency)

root = Tk()
root.title("Интерфейс модуля обработки данных с датчиков лесного робота с помощью ROS2")
root.iconbitmap('C:/Users/4792469/Desktop/CurrentSem/ТППО/ForestDaProM copy/RobotImage.ico')
root.geometry("425x150")

accelerometer_label = Label(root, text='Accelerometer')
accelerometer_label.grid()
label_xAccl = Label(root, text='xAccl = ?')
label_xAccl.grid()
label_yAccl = Label(root, text='yAccl = ?')
label_yAccl.grid()
label_zAccl = Label(root, text='zAccl = ?')
label_zAccl.grid()

magnitometer_label = Label(root, text='Magnitometer')
magnitometer_label.grid(column=1, row=0)
label_xMagn = Label(root, text='xMagn = 4')
label_xMagn.grid(column=1, row=1)
label_yMagn = Label(root, text='yMagn = 5')
label_yMagn.grid(column=1, row=2)
label_zMagn = Label(root, text='zMagn = 6')
label_zMagn.grid(column=1, row=3)

gyroscope_label = Label(root, text='Gyroscope')
gyroscope_label.grid(column=2, row=0)
label_xGyro = Label(root, text='xGyro = 1')
label_xGyro.grid(column=2, row=1)
label_yGyro = Label(root, text='yGyro = 8')
label_yGyro.grid(column=2, row=2)
label_zGyro = Label(root, text='zGyro = 4')
label_zGyro.grid(column=2, row=3)

lidar_label = Label(root, text='Lidar')
lidar_label.grid(column=3, row=0)

accelerometer_scale = Scale(root, from_=1, to=5, orient=HORIZONTAL)
accelerometer_scale.set(1)
accelerometer_scale.grid()

magnitometer_scale = Scale(root, from_=1, to=5, orient=HORIZONTAL)
magnitometer_scale.set(1)
magnitometer_scale.grid(column=1, row=4)

gyroscope_scale = Scale(root, from_=1, to=5, orient=HORIZONTAL)
gyroscope_scale.set(1)
gyroscope_scale.grid(column=2, row=4)

lidar_scale = Scale(root, from_=1, to=5, orient=HORIZONTAL)
lidar_scale.set(1)
lidar_scale.grid(column=3, row=4)

#danger_label = Label(root, text='Опасных ситуаций не наблюдается', bg='#afc')
#danger_label = Label(root, text='Опасные ситуации наблюдаются', bg='#fbc')
danger_label = Label(root, text='Наблюдается Тангаж с углом 35 градусов', bg='#fbc')
danger_label.grid(column=0, row=5, columnspan=4)

# Manage sensors
dispatcher = Dispatcher()
dispatcher.AddAccelerometer(0x53, 1)
dispatcher.AddGyro(0x68, 1)
dispatcher.AddMagnitometer(0x1e, 1)
dispatcher.StartThreads()

accelerometer_scale.bind("<ButtonRelease-1>", set_freq)

root.after(100, update)

root.mainloop()