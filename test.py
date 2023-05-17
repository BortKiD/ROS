import datetime
from time import sleep
from collections import deque

td = datetime.datetime(1,1,1)
date, time = td.now().isoformat().split("T")

data = deque()
for i in range(3):
    data.append((date, time, 0, 0, 0, 0))
    sleep(1)

for i in data:
    print(str(i).strip('()'))

print()
