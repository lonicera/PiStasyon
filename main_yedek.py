#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
sys.dont_write_bytecode = True
import datetime, time, logging, os
from functions import text_formatting
from dht22 import humtemp
import threading
zaman = datetime.datetime.now().time()
dakika = int(str(zaman)[3:-10])

deneme = True
def sensor():
    global deneme
    while deneme == True:
        print "deneme"
        time.sleep(0.1)
    print "oldu"     

text_formatting("Uygulama çalıştırıldı", 0, 'info')
values = []
interval_wd = 5
interval_ws = 5
interval_rg = 0.1
sensors = threading.Thread(target=sensor)
sensors.daemon = True
sensors.start()
while True:
    if dakika == 0:

        try: # collect data from sensors
            temp, hum = humtemp()
        except:
            text_formatting("Veriler tüm sensörlerden toplanamadı", 0, 'error')
        values.append([datetime.datetime.now(),temp, hum])        
    print values       
    time.sleep(0.1)
   
