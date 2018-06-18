#!/usr/bin/env python3
"""
RGB_pin->3,5
Ir_pin->37
"""
import RPi.GPIO as GPIO
import time
import sys
import json

#-----------------------DEF------------------------#
def initLEDPin(pin):
    GPIO.setup(pin, GPIO.OUT)
    pwm = GPIO.PWM(pin, 1000)
    pwm.start(0)
    return pwm

def getSignal(pin):
    start, stop = 0, 0
    signals = []

    while True:
        while GPIO.input(pin) == 0:
            None
    
        start = time.time()
    
        while GPIO.input(pin) == 1:
            stop = time.time()
            duringUp = stop - start
            if duringUp > 0.1 and len(signals) > 0:
                return signals[1:]
    
        signals.append(duringUp)

def compairSignal(s1, s2, rang):
    min_len = min(len(s1), len(s2))

    for i in range(min_len):
        if abs(s1[i] - s2[i]) > rang:
            return False
    
    return True

def decodeSignal(s, signal_map, rang):
    for name in signal_map.keys():
        if compairSignal(s, signal_map[name], rang):
            return name

    return None
#-----------------------MAIN------------------------#
def main():

# read key_map
    src = open("./key_map.json", 'r')
    signal_map = json.loads(src.read())
    src.close()

    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)

# Set IR_PIN
    GPIO.setup(37, GPIO.IN)

# init LED_PIN
    pwmr = initLEDPin(3)
    pwmg = initLEDPin(5)
    
# function introduce
    print("1    :LED on\n0    :LED off\nPower:poweroff\n\
+    :Plus Duty\n-    :Minus Duty")

    # start .........
    while True:  
        s = getSignal(37)
        sig=decodeSignal(s,signal_map,0.001)
        
        if sig == str('on'):
            print('----LED on----\n')
            duties=50
            pwmr.ChangeDutyCycle(duties)
            pwmg.ChangeDutyCycle(duties)
            shining=True
            while shining:
                ss = getSignal(37)
                sigg=decodeSignal(ss,signal_map,0.001)
                
                if sigg == str('plus'):
                    if duties==100:
                        print('duty limit :100')
                        continue
                    duties+=10
                    print('duty++  now duty:',duties)
                    pwmr.ChangeDutyCycle(duties)
                    pwmg.ChangeDutyCycle(duties)
                
                elif sigg == str('minus'):
                    if duties==0:
                        print('duty limit :0')
                        continue
                    duties-=10
                    print('duty--  now duty:',duties)
                    pwmr.ChangeDutyCycle(duties)
                    pwmg.ChangeDutyCycle(duties)
                
                elif sigg == str('off'):
                    print('----LED off----\n')
                    duties=0
                    pwmr.ChangeDutyCycle(duties)
                    pwmg.ChangeDutyCycle(duties)
                    shining=False
                elif sigg == str('power'):
                    print('Turn off the led first')

        elif sig == str('plus'):print('Turn on the led first')
        elif sig == str('minus'):print('Turn on the led first')
        elif sig == str('off'):print('Led is off now')
        elif sig == str('power'):
            print('----Good Bye----\n')
            break
        
        else:print('not record\n')
    
    # end
    pwmr.stop()
    pwmg.stop()
    GPIO.cleanup()
    
if __name__ == "__main__":
    main()