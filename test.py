import datetime
from time import sleep
from collections import deque
import csv

td = datetime.datetime(1,1,1)
date, time = td.now().isoformat().split("T")

data = deque()
for i in range(3):
    data.append((date, time, 0, 0, 0, 0))
    sleep(1)

with open('data.csv', 'w') as file:
    writer = csv.writer(file)
    writer.writerows(list(data))
