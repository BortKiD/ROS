import tkinter as tk
import os
import re 
import time
import subprocess
#os.system('ls')

centerX = 300
centerY = 300

radius = 4

root = tk.Tk()

frame1 = tk.Frame(root)
frame2 = tk.Frame(root)

frame1.pack(fill=tk.X)
frame2.pack(fill=tk.BOTH, expand=True)

build_button = tk.Button(frame1, text='Build map', command=lambda : print_points())
build_button.grid(row=0, column=0)

clear_button = tk.Button(frame1, text='Clear map', command=lambda : clear_canvas())
clear_button.grid(row=0, column=1)

scrollX = tk.Scrollbar(frame2, orient=tk.HORIZONTAL)
scrollY = tk.Scrollbar(frame2, orient=tk.VERTICAL)

canvas = tk.Canvas(frame2, background='white', xscrollcommand=scrollX.set, yscrollcommand=scrollY.set)
scrollX.config(command=canvas.xview)
scrollY.config(command=canvas.yview)
scrollX.pack(side = tk.BOTTOM)
scrollY.pack(side = tk.RIGHT)
canvas.pack(fill=tk.BOTH, expand=True)

def read_points():
    #get_distance = subprocess.Popen(['./urg_library/current/samples/cpp/get_distance', '>', 'Points.txt'])
    #get_distance.wait()
    os.system('python3 test_driver_laser.py')
    #os.system('./urg_library/current/samples/cpp/get_distance > Points.txt')
    #time.sleep(0.5)
    file = open('Points.txt', 'r')
    mas = []
    string = file.readline()
    string = file.readline()	
    while (string != ''):
        string = re.search(r'\(.*\)', string)
        if string: 
            string = string[0][1:-1]
            string = string.split(' ')
            string[0] = round((float)(string[0])/2, 0)
            string[1] = round((float)(string[1])/2, 0)
            mas.append(string)
        string = file.readline()
    file.close()
    return mas


def print_points():
    #os.system('./urg_library/current/samples/cpp/get_distance > Points.txt')
    while True:
        clear_canvas()
        mas = read_points()
        canvas.create_oval((int)(-radius/2)+centerX, (int)(-radius/2)+centerY, (int)(radius/2)+centerX, (int)(radius/2)+centerY, fill='red', outline='red')
        for item in mas:
            canvas.create_oval(item[0]-(int)(radius/2)+centerX, item[1]-(int)(radius/2)+centerY, item[0]+(int)(radius/2)+centerX, item[1]+(int)(radius/2)+centerY, fill='black', outline='black')
        root.update()
        canvas.update()
        #time.sleep(0.5)
def clear_canvas():
    canvas.delete('all')
    return
    while True:
        t1 = threading.Thread(target=print_points, daemon=True)
        #os.system('./urg_library/current/samples/cpp/get_distance > Points.txt')


root.mainloop()

