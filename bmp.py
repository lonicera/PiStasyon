#!/usr/bin/python
# -*- coding: utf-8 -*-
import Adafruit_BMP.BMP085 as BMP085
sensor = BMP085.BMP085(mode=BMP085.BMP085_ULTRAHIGHRES)

def get_BMP():
    temp = sensor.read_temperature()
    press = sensor.read_pressure() * 0.00750061683
    return temp, press
