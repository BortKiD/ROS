from API.PointClass import Point

p = Point(0, 0, 10, 30)
lst = [p, p, p]
x = [ i.X for i in lst ]

print(x)
