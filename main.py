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
        harray = []
        get_direction(ryonu)
    if "Rain" in veri:
        ygmr = veri.split()[2]
        ytop = ytop + float(ygmr)
    #if round(time.time()%120,1) == 120:
    if cur_time - last_up > interval and dakika == 0:
        #print "burada"
        tempe, hum = humtemp()
        temp, press = bastemp()
        last_up = cur_time
        if rtop > 0:
            rhizih = rtop / counter
        else:
            rhizih = 0
        values.extend((time.time(), datetime.datetime.now(),temp, hum, press, ytop, rhizih, hk, lght))
        values = values + wd
        try:
            if internet_on() and not offline:
                text_formatting("İnternet var ve sistem çevrimiçi", 0, 'info')
                gwrite(values)
                text_formatting("Veriler gdoca yazıldı", 0, 'info')
                #Tweet atalım bakalım
                if ytop > 5 and saat == 8:
                    send_main("Bu sabaaah yağmur var Zonguldak'ta. Yağış miktarı: " + str("ytop") + " mm" )
            elif internet_on() and offline:
                text_formatting("İnternet algılandı ve eski veriler yazılacak", 0, 'info')
                sqlin(values)
                sqltogsp()
                offline = False
            else:
                text_formatting("İnternet yok, çevrim dışı", 0, 'info')
                offline = True
                sqlin(values)   
        except Exception, e:
            text_formatting("Veriler kaydedilemedi ," + str(e), 0, 'error')
            pass
        counter = 0
        ytop = 0
        rtop = 0
        wd = [0,0,0,0,0,0,0,0]
        values = []
    time.sleep(0.1)
