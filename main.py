import datetime
from tkinter import *
from API.dispatcher import *
from DataStorage import *

def update():
    dataset = dispatcher.getDataset()

    xAccl, yAccl, zAccl = dataset.xAccl, dataset.yAccl, dataset.zAccl
    label_xAccl['text'] = 'xAccl = ' + "{:.2f}".format(xAccl)
    label_yAccl['text'] = 'yAccl = ' + "{:.2f}".format(yAccl)
    label_zAccl['text'] = 'zAccl = ' + "{:.2f}".format(zAccl)
    
    xMagn, yMagn, zMagn = dataset.xMagn, dataset.yMagn, dataset.zMagn
    label_xMagn['text'] = 'xMagn = ' + "{:.2f}".format(xMagn)
    label_yMagn['text'] = 'yMagn = ' + "{:.2f}".format(yMagn)
    label_zMagn['text'] = 'zMagn = ' + "{:.2f}".format(zMagn)

    xGyro, yGyro, zGyro = dataset.xGyro, dataset.yGyro, dataset.zGyro
    label_xGyro['text'] = 'xGyro = ' + "{:.2f}".format(xGyro)
    label_yGyro['text'] = 'yGyro = ' + "{:.2f}".format(yGyro)
    label_zGyro['text'] = 'zGyro = ' + "{:.2f}".format(zGyro)

    pitch, roll, yaw = dataset.Pitch, dataset.Roll, dataset.Yaw
    label_pitch['text'] = 'pitch = ' + "{:.2f}".format(pitch)
    label_roll['text'] = 'roll = ' + "{:.2f}".format(roll)
    label_yaw['text'] = 'yaw = ' + "{:.2f}".format(yaw)

    if (pitch > 35 or pitch < -35):
        danger_label['bg'] = "#fbc"
        danger_label['text'] = "Опасная ситуация"
    else:
        danger_label['bg'] = "#afc"
        danger_label['text'] = "Нет опасной ситуации"

    root.after(100, update)

def set_freq(e):
    frequency = accelerometer_scale.get()
    dispatcher.AcclFreq = frequency

    frequency = gyroscope_scale.get()
    dispatcher.GyroFreq = frequency

    frequency = magnitometer_scale.get()
    dispatcher.MagnFreq = frequency

root = Tk()
root.title("Интерфейс модуля обработки данных с датчиков лесного робота с помощью ROS2")
root.iconbitmap('C:/Users/4792469/Desktop/CurrentSem/TPPO/ForestDaProM copy/RobotImage.ico')
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
label_xMagn = Label(root, text='xMagn = ?')
label_xMagn.grid(column=1, row=1)
label_yMagn = Label(root, text='yMagn = ?')
label_yMagn.grid(column=1, row=2)
label_zMagn = Label(root, text='zMagn = ?')
label_zMagn.grid(column=1, row=3)

gyroscope_label = Label(root, text='Gyroscope')
gyroscope_label.grid(column=2, row=0)
label_xGyro = Label(root, text='xGyro = ?')
label_xGyro.grid(column=2, row=1)
label_yGyro = Label(root, text='yGyro = ?')
label_yGyro.grid(column=2, row=2)
label_zGyro = Label(root, text='zGyro = ?')
label_zGyro.grid(column=2, row=3)

angle_label = Label(root, text='Angle')
angle_label.grid(column=3, row=0)
label_pitch = Label(root, text='Pitch = ?')
label_pitch.grid(column=3, row=1)
label_roll = Label(root, text='Roll = ?')
label_roll.grid(column=3, row=2)
label_yaw = Label(root, text='Yaw = ?')
label_yaw.grid(column=3, row=3)

lidar_label = Label(root, text='Lidar')
lidar_label.grid(column=4, row=0)

accelerometer_scale = Scale(root, from_=1, to=5, orient=HORIZONTAL)
accelerometer_scale.set(1)
accelerometer_scale.grid()

magnitometer_scale = Scale(root, from_=1, to=5, orient=HORIZONTAL)
magnitometer_scale.set(1)
magnitometer_scale.grid(column=1, row=4)

gyroscope_scale = Scale(root, from_=1, to=5, orient=HORIZONTAL)
gyroscope_scale.set(1)
gyroscope_scale.grid(column=2, row=4)

angle_scale = Scale(root, from_=1, to=5, orient=HORIZONTAL)
angle_scale.set(1)
angle_scale.grid(column=3, row=4)

lidar_scale = Scale(root, from_=1, to=5, orient=HORIZONTAL)
lidar_scale.set(1)
lidar_scale.grid(column=4, row=4)

danger_label = Label(root, text='Нет опасной ситуации', bg='#fbc')
danger_label.grid(column=0, row=5, columnspan=4)

# Manage sensors
dispatcher = Dispatcher()
dispatcher.AddAccelerometer(0x53, 1)
dispatcher.AddGyro(0x68, 1)
dispatcher.AddMagnitometer(0x1e, 1)
dispatcher.StartThreads()

accelerometer_scale.bind("<ButtonRelease-1>", set_freq)
magnitometer_scale.bind("<ButtonRelease-1>", set_freq)
gyroscope_scale.bind("<ButtonRelease-1>", set_freq)

root.after(100, update)

root.mainloop()

exit()