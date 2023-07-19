###############################################################
##  Simple code to use PWM on the PI to control the BTS7960
## 
##  This simply spins the motor in one direction slowly 
##  speeding up slowly and then slowing down slowly over
##  and over again.
##
###############################################################

import RPi.GPIO as GPIO
# https://sourceforge.net/p/raspberry-gpio-python/wiki/PWM/


import time


# We are going to use the BCM not BOARD layout
# https://i.stack.imgur.com/yHddo.png - BCM are the "GPIO#" ones not the ordered pins
GPIO.setmode(GPIO.BCM)  
GPIO.setwarnings(False)


RPWM = 13;  # GPIO pin 19 to the RPWM on the BTS7960
LPWM = 19;  # GPIO pin 26 to the LPWM on the BTS7960

# For enabling "Left" and "Right" movement
L_EN = 5;  # connect GPIO pin 20 to L_EN on the BTS7960
R_EN = 6;  # connect GPIO pin 21 to R_EN on the BTS7960


# Set all of our PINS to output
GPIO.setup(RPWM, GPIO.OUT)
GPIO.setup(LPWM, GPIO.OUT)
GPIO.setup(L_EN, GPIO.OUT)
GPIO.setup(R_EN, GPIO.OUT)


# Enable "Left" and "Right" movement on the HBRidge
GPIO.output(R_EN, True)
GPIO.output(L_EN, True)


rpwm= GPIO.PWM(RPWM, 50)
lpwm= GPIO.PWM(LPWM, 50)

rpwm.ChangeDutyCycle(0)
rpwm.start(0) 

while 1:
    
  for x in range(50):
    print("Speeding up " + str(x))
    rpwm.ChangeDutyCycle(x)
    time.sleep(0.05)

  time.sleep(5)
  rpwm.ChangeDutyCycle(0)

#  for x in range(50):

#    print("Slowing down " + str(x))
#    rpwm.ChangeDutyCycle(50-x)
#    time.sleep(0.05)
    
  lpwm.start(0)
  for x in range(50):
    print("Speeding up " + str(x))
    lpwm.ChangeDutyCycle(x)
    time.sleep(0.05)
  
    
  time.sleep(5)
  lpwm.ChangeDutyCycle(0)
#  for x in range(50):

#    print("Slowing down " + str(x))
#    lpwm.ChangeDutyCycle(50-x)
#    time.sleep(0.05)
