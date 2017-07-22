#!/usr/bin/python
#
# This script reads from a joystick and 4x4 touchpad-
# then plays music files depending on the physical inputs.
# This is a work in progress! 
# Use at your own risk.
#
#--------------------------------------   
# Credit for the Joystick input code:
# 
# This script reads data from a 
# MCP3008 ADC device using the SPI bus.
#
# Analogue joystick version!
#
# Author : Matt Hawkins
# Date   : 17/04/2014
#
# http://www.raspberrypi-spy.co.uk/
#
#--------------------------------------

import spidev
import time
import os
import pygame
import atexit
from pad4pi import rpi_gpio

# Adding an exit handler for cleanup

def exit_handler():
  print('Cleaning up....')
  keypad.cleanup()

atexit.register(exit_handler)

# Keypad Setup

KEYPAD = [
        ["1","2","3","A"],
        ["4","5","6","B"],
        ["7","8","9","C"],
        ["*","0","#","D"]
]

COL_PINS = [6,13,19,26] # BCM numbering on Raspberry Pi 3 and Zero
ROW_PINS = [16,20,21,5] # BCM numbering on Raspberry Pi 3 and Zero

factory = rpi_gpio.KeypadFactory()

keypad = factory.create_keypad(keypad=KEYPAD, row_pins=ROW_PINS, col_pins=COL_PINS)

#keypad.registerKeyPressHandler(processKey)

def processKey(key):
  if (key=="1"):
    print("number 1")
  else:
    print(key)

# PyGame Audio Mixer setup - load in all music files
pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.mixer.init()
pygame.init()
pygame.mixer.music.load('test.wav')

# Open SPI bus
spi = spidev.SpiDev()
spi.open(0,0)

# Function to read SPI data from MCP3008 chip
# Channel must be an integer 0-7
def ReadChannel(channel):
  adc = spi.xfer2([1,(8+channel)<<4,0])
  data = ((adc[1]&3) << 8) + adc[2]
  return data
 
# Define sensor channels
# (channels 3 to 7 unused)
swt_channel = 0
vrx_channel = 1
vry_channel = 2

# Define delay between readings (s)
delay = 0.5

while True:
  # Register keypad
  keypad.registerKeyPressHandler(processKey)

  # Read the joystick position data
  vrx_pos = ReadChannel(vrx_channel)
  vry_pos = ReadChannel(vry_channel)

  # Read switch state
  swt_val = ReadChannel(swt_channel)

  # Print out results
  # print "--------------------------------------------"  
  # print("X : {}  Y : {}  Switch : {}".format(vrx_pos,vry_pos,swt_val))
  
  if (swt_val < 10):
    print "switch pressed" 	
    pygame.mixer.music.play(1,0.0)
  # X: <10 means X is to the left
  # X: >700 means X is to the right
  # Y: <10 means Y is down
  # Y: >700 means Y is up
  # Switch: <10 means switch is pressed

  # Wait before repeating loop
  time.sleep(delay)

