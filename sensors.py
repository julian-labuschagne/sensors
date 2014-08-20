#!/usr/bin/python

import RPi.GPIO as GPIO
import spidev
import time
import os

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(True)
GPIO.cleanup()

# Setup Pins
gpio_pins = [22, 27, 17, 23, 24, 25]
for gpio_pin in gpio_pins
    GPIO.setup(gpio_pin, GPIO.OUT)

# Turn Leds off
GPIO.output(22, GPIO.LOW)
GPIO.output(27, GPIO.LOW)
GPIO.output(17, GPIO.LOW)

GPIO.output(23, GPIO.LOW)
GPIO.output(24, GPIO.LOW)
GPIO.output(25, GPIO.LOW)

# Open SPI bus
spi = spidev.SpiDev()
spi.open(0,0)

# Function to read SPI data from MCP3008 chip
# Channel must a integer between 0-7
def ReadChannel(channel):
    adc = spi.xfer2([1,(8+channel)<<4,0])
    data = ((adc[1]&3) << 8) + adc[2]
    return data

# Define sensor channels
light_channel = 0
pot_channel = 1

# Define delay between readings
delay = .5

while True:
    # Read the light sensor data
    light_level = ReadChannel(light_channel)
    if(light_level < 256):
        GPIO.output(23, GPIO.LOW)
        GPIO.output(24, GPIO.LOW)
        GPIO.output(25, GPIO.LOW)
    elif(light_level < 512) and (light_level > 256):
        GPIO.output(23, GPIO.HIGH)
        GPIO.output(24, GPIO.LOW)
        GPIO.output(25, GPIO.LOW)
    elif(light_level < 768) and (light_level > 512):
        GPIO.output(23, GPIO.HIGH)
        GPIO.output(24, GPIO.HIGH)
        GPIO.output(25, GPIO.LOW)
    elif(light_level < 1024) and (light_level > 768):
        GPIO.output(23, GPIO.HIGH)
        GPIO.output(24, GPIO.HIGH)
        GPIO.output(25, GPIO.HIGH)

    # Read the pot data
    pot_level = ReadChannel(pot_channel)
    if(pot_level < 256):
        GPIO.output(22, GPIO.LOW)
        GPIO.output(27, GPIO.LOW)
        GPIO.output(17, GPIO.LOW)
    elif(pot_level < 512) and (pot_level > 256):
        GPIO.output(22, GPIO.HIGH)
        GPIO.output(27, GPIO.LOW)
        GPIO.output(17, GPIO.LOW)
    elif(pot_level < 768) and (pot_level > 512):
        GPIO.output(22, GPIO.HIGH)
        GPIO.output(27, GPIO.HIGH)
        GPIO.output(17, GPIO.LOW)
    elif(pot_level < 1024) and (pot_level > 768):
        GPIO.output(22, GPIO.HIGH)
        GPIO.output(27, GPIO.HIGH)
        GPIO.output(17, GPIO.HIGH)

    # Print our results
    print "--------------------"
    print ("Light: {}".format(light_level))
    print ("Pot: {}".format(pot_level))

    # Wait before repeating loop
    time.sleep(delay)
    os.system('clear')
