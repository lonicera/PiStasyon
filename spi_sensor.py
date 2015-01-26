#!/usr/bin/python
# -*- coding: utf-8 -*- 
import spidev
import time
import os
 
# Open SPI bus
spi = spidev.SpiDev()
spi.open(0,0)
 
# Function to read SPI data from MCP3008 chip
# Channel must be an integer 0-7
def ReadChannel(channel):
  adc = spi.xfer2([1,(8+channel)<<4,0])
  data = ((adc[1]&3) << 8) + adc[2]
  return data
 
# Function to convert data to voltage level,
# rounded to specified number of decimal places.
def ConvertVolts(data,places):
  volts = (data * 3.3) / float(4096)
  volts = round(volts,places)
  return volts
 

def read_sensor(i):
 
  # Read the light sensor data
  sensor_level = ReadChannel(i)
  sensor_volts = ConvertVolts(sensor_level,2)
  return float(sensor_volts)
