#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
sys.dont_write_bytecode = True
import datetime, time, logging, os
from functions import text_formatting, gwrite, sqlin, sqltogsp, internet_on, send_mail, get_interface_ip, mysqlin
from dht22 import humtemp
from baro import bastemp
from spi_sensor import read_sensor

   
last_upt_wd = time.time()
text_formatting("Uygulama çalıştırıldı", 0, 'info')
values = []
interval_wd = 5
interval_rg = 0.1
wd = [0,0,0,0,0,0,0,0]
ws = 0
rg = 0
hk = 0
light = 0
offline = False
send_mail(get_interface_ip('eth0'))
ykilit = False
while True:
    if time.time() >= last_upt_wd + interval_wd:
       last_upt_wd = time.time()
       if read_sensor(0) >= 0.61 and read_sensor(0) <= 0.63:
           wd[0] = int(wd[0]) + 1
       elif read_sensor(0) >= 0.68 and read_sensor(0) <= 0.72:
           wd[1] = int(wd[1]) + 1
       elif read_sensor(0) >= 0.73 and read_sensor(0) <= 0.77:
           wd[2] = int(wd[2]) + 1
       elif read_sensor(0) >= 0.48 and read_sensor(0) <= 0.53:
           wd[3] = int(wd[3]) + 1
       elif read_sensor(0) >= 0.21 and read_sensor(0) <= 0.25:
           wd[4] = int(wd[4]) + 1
       elif read_sensor(0) >= 0.13 and read_sensor(0) <= 0.17:
           wd[5] = int(wd[5]) + 1
       elif read_sensor(0) >= 0.06 and read_sensor(0) <= 0.10:
           wd[6] = int(wd[6]) + 1
       elif read_sensor(0) >= 0.34 and read_sensor(0) <= 0.39:
           wd[7] = int(wd[7]) + 1
    if read_sensor(7) > 0.2:
        ws = ws + 1 
    if read_sensor(6) < 0.4  and not ykilit:
        rg = rg + 1
        ykilit = True
    if ykilit and 2.1-time.time()%2.1 < 0.1:
        ykilit = False
    if 3600-time.time()%3600 < 0.2:                   
        text_formatting("Veri girme saati", 0, 'info')
        last_upt_ws = time.time()
        try: # collect data from sensors
            try:
                tempe, hum = humtemp()
                temp, press = bastemp()
                hk = read_sensor(3)
                light = read_sensor(4)
                text_formatting("Veriler toplandı", 0, 'info')
            except Exception, e:
                text_formatting("Veriler toplanamadı. " + str(e) , 0, 'info')
                pass 
            wsc = ws * 0.000666667 
            #wsc = ws
            rgc = rg * 0.2794
            #rgc = rg
            values.extend((time.time(),tempe, hum, press, rgc, wsc, hk, light))
            values = values + wd
            try:
                if internet_on() and not offline:
                    text_formatting("İnternet var ve sistem çevrimiçi", 0, 'info')
                    gwrite(values)
                    text_formatting("Veriler gdoca yazıldı", 0, 'info')
                elif internet_on() and offline:
                    text_formatting("İnternet algılandı ve eski veriler yazılacak", 0, 'info')
                    sqlin(values)
                    sqltogsp()
                    offline = False
                else:
                    text_formatting("İnternet yok, çevrim dışı", 0, 'info')
                    offline = True
                    sqlin(values)   
            except:
                text_formatting("Veriler kaydedilemedi", 0, 'error')
                pass
            ws = 0
            rg = 0
            wd = [0,0,0,0,0,0,0,0]
            values = []
        except:
            text_formatting("Veriler tüm sensörlerden toplanamadı", 0, 'error')
            pass
    time.sleep(0.1)
   
