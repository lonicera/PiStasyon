  GNU nano 2.2.6                          File: amet/main.py                                                          

#!/usr/bin/python
# -*- coding: utf-8 -*-
import serial, time, urllib2, sys
from functions import text_formatting, gwrite, sqlin, sqltogsp, internet_on, send_mail, get_interface_ip, mysqlin
import datetime, time, logging, os
from dht22 import humtemp
from baro import bastemp
from spi_sensor import read_sensor
from twit import send_main
sys.dont_write_bytecode = True
ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
ygmr = 0
wd = [0,0,0,0,0,0,0,0]
counter = 0
rtop = 0
ytop = 0
rhizih = 0
last_up = time.time()
text_formatting("Uygulama çalıştırıldı", 0, 'info')
values = []
offline = False
interval = 90
def get_direction (ryonu):
    if "NW" in ryonu:
        wd[1] = int(wd[1]) + 1
    elif "NE" in ryonu:
        wd[7] = int(wd[7]) + 1
    elif "N" in ryonu:
        wd[0] = int(wd[0]) + 1
    elif "SW" in ryonu:
        wd[3] = int(wd[3]) + 1
    elif "SE" in ryonu:
        wd[5] = int(wd[5]) + 1
    elif "S" in ryonu:
        wd[4] = int(wd[4]) + 1
    elif "W" in ryonu:
        wd[2] = int(wd[2]) + 1
    elif "E" in ryonu:
        wd[6] = int(wd[6]) + 1

while True:
    zaman = datetime.datetime.now().time()
    dakika = int(str(zaman)[3:-10])
    saat = int(str(zaman)[:-13])
    cur_time = time.time()
    veri = ser.readline().rstrip('\n')
    if "Wind" in veri:
        counter = counter + 1
        rhizi = float(veri.split()[2]) / 10
        ryonu = veri.split()[5]
        rtop = rtop + float(rhizi)
        hk = read_sensor(3)
        lght = read_sensor(4)
                                                  [ Read 97 lines ]
^G Yardım Al       ^O Yaz             ^R Dosya Oku       ^Y Önceki Sayfa    ^K Metni Kes       ^C İmleç Pozisyonu
^X Çık             ^J Yasla           ^W Ara             ^V Sonraki Sayfa   ^U UnCut Text      ^T Denetime
