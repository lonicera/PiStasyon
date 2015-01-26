from spi_sensor import read_sensor
import os, time
clear = lambda: os.system('clear')
ykilit = False
rzg = 0
ygr = 0
rzgh=0
aygr = 0
while True:
    global rzg
    if read_sensor(7) < 0.5:
        rzg = rzg + 1
    if read_sensor(6) < 0.4 and not ykilit:
        ygr = ygr + 1
        aygr = aygr + 1
        ykilit = True
    if ykilit and 2.1-time.time()%2.1 < 0.1:
        ykilit = False
    clear()
    if 2.1-time.time()%2.1 < 0.1:
        rzgh = rzg*2.4 / 5
        rzg = 0
    if 3600-time.time()%3600 < 0.1:
        ygr = 0
    if 20.1-time.time()%20.1 < 0.1:
        aygr = 0
    print "Ruzgar: " + str(rzgh) + " km/s"
    print "Yagmur: " + str(ygr) + " mm" + "Anlik: " + str(aygr)
    print read_sensor(4)
    time.sleep(0.1)   


