from datetime import datetime as dt
import time

print(dt.timetuple(dt.now()))
a = time.mktime((2018, 10, 28, 3, 51, 30, 0, 0, 0))
a1 = time.mktime((2018, 10, 28, 3, 59, 29, 0, 0, 0))
a2 = time.mktime((2018, 10, 28, 3, 51, 29, 0, 0, 0))
b = time.mktime((2018, 10, 28, 4, 42, 23, 0, 0, 0))
print(a)
print(a1)
print(a2)
print(b)

