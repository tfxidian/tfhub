import datetime
import time
t = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
print t

dt = "2016-05-05 20:28:54"
dd = '2017-8-14 10:29:47:11063'

print dd
timeArray = time.strptime(dd, "%Y-%m-%d %H:%M:%S:%f")

timestamp = time.mktime(timeArray)

print timestamp