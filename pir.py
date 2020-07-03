#  Bewegungsmelder schaltet Monitor vom Raspberry Pi aus und an
#!/usr/bin/python


# Import der Python libraries
import RPi.GPIO as GPIO
import time
import datetime
import subprocess


# Verwendung des Board Mode, Angabe der PIN Nummern anstelle der GPIO BCM Nummer
GPIO.setmode(GPIO.BOARD)


# GPIO definieren, bei mir ist es PIN 8
GPIO_PIR = 8


#  GPIO als "Input" festlegen
GPIO.setup(GPIO_PIR,GPIO.IN)


Current_State  = 0
Previous_State = 0


try:


# erst mal schlafen bis der bootvorgang abgeschlossen ist
time.sleep(60)


# Warten bis Sensor sich meldet
while GPIO.input(GPIO_PIR)==1:
  Current_State  = 0


subprocess.Popen('echo initilized PIR | wall', shell=True)


# Schleife bis CTRL+C
while True :


  #Status von Sensor auslesen
  Current_State = GPIO.input(GPIO_PIR)


  if Current_State==1 and Previous_State==0:


    # Kommando zum anschalten, Frambuffer erneuern
    subprocess.Popen('echo Monitor on | wall', shell=True)
    subprocess.Popen('/opt/vc/bin/tvservice -p', shell=True)
    subprocess.Popen('fbset -depth 8', shell=True)
    subprocess.Popen('fbset -depth 16', shell=True)
    subprocess.Popen('sudo /bin/chvt 6 && sudo /bin/chvt 7', shell=True)
    Previous_State=1


  elif Current_State==0 and Previous_State==1:


    # Ausschalten des Monitors
    subprocess.Popen('echo Monitor off | wall', shell=True)
    subprocess.Popen('/opt/vc/bin/tvservice -o', shell=True)
    Previous_State=0


  # 5 Sek Warten
  time.sleep(5)


except KeyboardInterrupt:
print " Exit"
GPIO.cleanup()