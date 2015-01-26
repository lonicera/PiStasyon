#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
sys.dont_write_bytecode = True
import datetime, time, logging, os
from functions import text_formatting, gwrite, sqlin, sqlite3


values = []
wd = [0,0,0,0,0,0,0,0]
ws = 0
rg = 0
hk = 0
lght = 0
temp = 999
hum = 9999
press = 9999
hk = 0
lght = 0
wsc = 22
rg = 20
rgc = rg * 0.2794
values.extend((datetime.datetime.now(),temp, hum, press, rgc, wsc, hk, lght))
values = values + wd
db = sqlite3.connect("aeromet.sqlite")
cursor = db.cursor()
for i in cursor.execute('''select tarih, sicaklik, nem, basinc, yagis, rhizi, hkalite, isik, K, KB, B, GB, G, GD, D, KD from temp ORDER BY id asc'''):
    gwrite(i)
    #text_formatting(i, 1, 'info')
    time.sleep(0.5)
#row = cursor.fetchall()
cursor.execute('''delete  from temp''')
db.commit()

