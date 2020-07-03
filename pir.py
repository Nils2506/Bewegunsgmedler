#!/usr/bin/env python

import sys
import time
import RPi.GPIO as io
import subprocess

io.setmode(io.BCM)
SHUTOFF_DELAY = 60 # seconds
PIR_PIN = 25       # 22 on the board
LED_PIN = 16

def main():
    io.setup(PIR_PIN, io.IN)
    io.setup(LED_PIN, io.OUT)
    turned_off = False
    last_motion_time = time.time()

    while True:
        if io.input(PIR_PIN):
            last_motion_time = time.time()
            io.output(LED_PIN, io.LOW)
            print ".",
            sys.stdout.flush()
            if turned_off:
                turned_off = False
                turn_on()
        else:
            if not turned_off and time.time() > (last_motion_time + 
                                                 SHUTOFF_DELAY):
                turned_off = True
                turn_off()
            if not turned_off and time.time() > (last_motion_time + 1):
                io.output(LED_PIN, io.HIGH)
        time.sleep(.1)

def turn_on():
    subprocess.call("sh /home/pi/photoframe/monitor_on.sh", shell=True)

def turn_off():
    subprocess.call("sh /home/pi/photoframe/monitor_off.sh", shell=True)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        io.cleanup()
Turning the monitor on and off
There are two ways to turn the monitor on and off. Use the tvservice command to turn off the monitor port.

pi@raspberrypi ~/photoframe $ chmod 0744 monitor_off.sh 
pi@raspberrypi ~/photoframe $ cat monitor_off.sh 
tvservice -o

pi@raspberrypi ~/photoframe $ chmod 0744 monitor_on.sh 
pi@raspberrypi ~/photoframe $ cat monitor_on.sh 
tvservice -c "PAL 4:3" && fbset -depth 8 && fbset -depth 16